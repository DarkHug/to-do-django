import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail

from .models import Task, User
from .forms import TaskForm, SignUpForm, VerificationForm
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
        if user.is_confirmed:
            if user is not None:
                login(request, user)
                messages.success(request, 'You Have Log In')
                return redirect('all_task')
            else:
                return redirect('login')
        else:
            return redirect('verification')
    return render(request, 'login.html')


def generate_verification_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            verification_code = generate_verification_code()
            user.verification_code = verification_code
            user.save()
            send_mail(
                "Verification",
                f"This is your code {verification_code}",
                "from@example.com",
                ["to@example.com"],
                fail_silently=False,
            )
            return redirect('verification')
    else:
        form = SignUpForm
    return render(request, 'register.html', {'form': form})


def verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                user = User.objects.get(verification_code=code)
                user.is_confirmed = True
                user.verification_code = ''
                user.save()
                login(request, user)
                messages.success(request, 'Congratulations You Created Account')
                return redirect('all_task')
            except:
                messages.error(request, 'Wrong Code')
                form.add_error('code', 'Invalid verification code')
    else:
        form = VerificationForm()
    return render(request, 'verification.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')
