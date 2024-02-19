from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages


def home_page(request):
    return render(request, 'home.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')


def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username is already taken. Please choose another.')
            else:
                User.objects.create_user(username=username, password=password, name=name)
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')

        else:
            messages.warning(request, 'Passwords did not match. Please try again.')

    return render(request, 'register.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def donate_user(request):
    return render(request, 'donate.html')


def johnstown_2024_page(request):
    # Your view logic goes here
    return render(request, 'Johnstown2024.html')

def registration_page(request):
    # Your view logic goes here
    return render(request, 'registration.html')