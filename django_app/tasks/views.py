from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db import transaction
import logging
from .models import Task
from .forms import TaskForm
from .kafka_utils import send_task_to_kafka

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    tasks = Task.objects.filter(user=request.user)
    pending_tasks = tasks.filter(status='pending', suggested=False)
    completed_tasks = tasks.filter(is_completed=True)
    overdue_tasks = tasks.filter(due_date__lt=timezone.now(), is_completed=False)

    # Suggested tasks (from Gmail) that are waiting for user action
    suggested_tasks = tasks.filter(suggested=True)
    context = {
        'tasks': tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'suggested_tasks': suggested_tasks,  
        'total_tasks': tasks.count(),
        'pending_count': pending_tasks.count(),
        'completed_count': completed_tasks.count(),
        'overdue_count': overdue_tasks.count(),
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def add_task(request):
    """Add new task with Kafka event."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            try:
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                logger.info(f"Task created: {task.id} by {request.user.username}")
                
                # Send to Kafka asynchronously
                try:
                    send_task_to_kafka({
                        "task_id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "due_date": task.due_date.isoformat(),
                        "priority": task.priority,
                        "status": task.status,
                        "is_completed": task.is_completed,
                        "user": task.user.username,
                        "created_at": task.created_at.isoformat(),
                    })
                except Exception as e:
                    logger.error(f"Error sending task to Kafka: {str(e)}")
                    # Don't fail the response, task is still created in DB

                return redirect('dashboard')
            except Exception as e:
                logger.error(f"Error creating task: {str(e)}")
                form.add_error(None, "Error creating task. Please try again.")
    else:
        form = TaskForm()
    
    return render(request, 'tasks/add_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    """Edit an existing task."""
    try:
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                form.save()
                logger.info(f"Task {task_id} updated by {request.user.username}")
                return redirect('dashboard')
        else:
            form = TaskForm(instance=task)
        return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})
    except Exception as e:
        logger.error(f"Error editing task {task_id}: {str(e)}")
        return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    """Delete a task."""
    try:
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        if request.method == 'POST':
            logger.info(f"Task {task_id} deleted by {request.user.username}")
            task.delete()
            return redirect('dashboard')
        return render(request, 'tasks/confirm_delete.html', {'task': task})
    except Exception as e:
        logger.error(f"Error deleting task {task_id}: {str(e)}")
        return redirect('dashboard')


def signup_view(request):
    """User registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                logger.info(f"New user registered: {username}") 
                return redirect('dashboard')
            except Exception as e:
                logger.error(f"Error during signup: {str(e)}")
                form.add_error(None, "Error creating account. Please try again.")
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


def speak_assistant(request):
    actions = [
        "Open YouTube",
        "Search Google",
        "Open Slack",
        "Open WhatsApp Web",
        "Create Google Doc",
        "Open Zoom",
        "Open GitHub" , 
        "Open LinkedIn",
        "adding more..."
    ]
    return render(request, 'tasks/speak_assistant.html', {"actions": actions})

