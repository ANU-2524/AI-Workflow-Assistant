from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from .kafka_utils import send_task_to_kafka


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
    """Add new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            print("Sending to Kafka -->")
            send_task_to_kafka({
                        "title": task.title,
                        "description": task.description,
                        "due_date": task.due_date.isoformat(),
                        "priority": task.priority,
                        "status": task.status,
                        "is_completed": task.is_completed,
                        "user": task.user.username,
                        "created_at": task.created_at.isoformat(),
                    })

            return redirect('dashboard')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/add_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')
    return render(request, 'tasks/confirm_delete.html', {'task': task})


def signup_view(request):
    """User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


def speak_assistant(request):
    # Optionally pass actions list/context
    actions = ["Open YouTube", "Search Google", "Send Slack Message", "Open WhatsApp Web", "Create Google Doc", "Schedule Zoom", "Summarize Emails", "...etc"]
    return render(request, "tasks/speak_assistant.html", {"actions": actions})
