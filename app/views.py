from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Participant
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
            # Redirect to the dashboard with the participant's basic information
            return redirect('dashboard')
        else:
            messages.warning(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def donate_user(request):
    return render(request, 'donate.html')


def johnstown_2024_page(request):
    return render(request, 'johnstown2024.html')


def registration_page(request):
    if request.method == 'POST':
        # Extract data from the form
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        fundraising_goal = request.POST.get('fundraising_goal')
        donation_amount = request.POST.get('donation_amount', 0)  # Default to 0 if not provided
        team_option = request.POST.get('team_option')
        team_name = request.POST.get('team_name', '') if team_option == 'start_team' else ''
        under_18 = request.POST.get('under_18') == 'yes'
        mailing_address = request.POST.get('mailing_address')
        zip_code = request.POST.get('zip_code')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        phone_number = request.POST.get('phone_number', '')  # Optional field

        if password == confirm_password:
            # Check if the username is already taken
            if Participant.objects.filter(username=username).exists():
                messages.warning(request, 'Username is already taken. Please choose another.')
            else:
                # Create a Participant object and save it to the database
                Participant.objects.create_user(
                    name=name,
                    username=username,
                    password=password,
                    fundraising_goal=fundraising_goal,
                    donation_amount=donation_amount,
                    team_option=team_option,
                    team_name=team_name,
                    under_18=under_18,
                    mailing_address=mailing_address,
                    zip_code=zip_code,
                    city=city,
                    state=state,
                    country=country,
                    phone_number=phone_number
                )
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')

        else:
            messages.warning(request, 'Passwords did not match. Please try again.')

    return render(request, 'registration.html')  # Update with your actual template name


def dashboard(request):
    return render(request, 'dashboard.html')

def eventinyourcity(request):
    return render(request, 'eventinyourcity.html')
