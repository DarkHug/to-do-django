from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Task
from .forms import TaskForm, SignUpForm
from django.contrib.auth import login, authenticate, logout


def home(request):
    return render(request, 'home.html', {})


@login_required
def show_task(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'all_tasks.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('all_task')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})


@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('all_task')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'id': id})


def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        task.delete()
        return redirect('all_task')
    return redirect('all_task')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('all_task')
        else:
            return redirect('login')
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('all_task')
    else:
        form = SignUpForm
    return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')
