from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Task
from .forms import TaskForm

@login_required
def dashboard(request):
    """Main dashboard view showing tasks and schedules"""
    # Get user's tasks
    tasks = Task.objects.filter(user=request.user)
    pending_tasks = tasks.filter(status='pending')
    completed_tasks = tasks.filter(status='completed')
    overdue_tasks = tasks.filter(due_date__lt=timezone.now(), is_completed=False)
    
    # Dummy upcoming schedules for now
    upcoming_schedules = [
        {'title': 'Team Meeting', 'time': '10:00 AM', 'date': 'Today'},
        {'title': 'Project Review', 'time': '2:00 PM', 'date': 'Tomorrow'},
        {'title': 'Client Call', 'time': '11:00 AM', 'date': 'Friday'},
    ]
    
    context = {
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'upcoming_schedules': upcoming_schedules,
        'total_tasks': tasks.count(),
        'completed_count': completed_tasks.count(),
        'pending_count': pending_tasks.count(),
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
            return redirect('dashboard')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/add_task.html', {'form': form})

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
