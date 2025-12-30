from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'tasks/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    total = tasks.count()
    completed = tasks.filter(completed=True).count()
    pending = total - completed

    context = {
        'tasks': tasks,
        'total': total,
        'completed': completed,
        'pending': pending,
    }
    return render(request, 'tasks/dashboard.html', context)

@login_required
def add_task(request):
    if request.method == 'POST':
        Task.objects.create(
            user=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            priority=request.POST['priority'],
            due_date=request.POST['due_date']
        )
        return redirect('dashboard')
    return render(request, 'tasks/add_task.html')

@login_required
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return redirect('dashboard')


@login_required(login_url='login')
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.due_date = request.POST.get('due_date')
        task.save()
        return redirect('dashboard')

    return render(request, 'tasks/edit_task.html', {'task': task})
