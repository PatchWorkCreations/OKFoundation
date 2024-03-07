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
            if request.user.is_superuser:
                # Redirect to the admin dashboard
                return redirect('admin_dashboard')
            else:
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
        email = request.POST.get('email')
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
                    email=email,
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


def update_user(request):
    if request.method == 'POST':
        # Retrieve the form data
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        fundraising_goal = request.POST.get('fundraising_goal')

        # Update the user profile
        request.user.name = name
        request.user.username = username
        request.user.email = email
        request.user.fundraising_goal = fundraising_goal
        request.user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('dashboard')


def update_account_settings(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        # Update username if provided
        if username and username != user.username:
            user.username = username
            user.save()
            messages.success(request, 'Username successfully updated.')
            return redirect('dashboard')

        # Update password if provided
        if new_password and confirm_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password successfully updated.')
            # For security, log the user out after changing the password
            return redirect('logout')  # You should have a 'logout' URL defined in your urls.py


def admin_dashboard(request):
    participants = Participant.objects.all()
    participants_count = participants.count() - 1

    return render(request, 'admin_dashboard.html',
                  {'participants': participants, 'participants_count': participants_count})


def fetch_user_details(request, pk):
    participant = Participant.objects.get(id=pk)

    return render(request, 'fetch_user_details.html', {'participant': participant})


def update_user_detail(request, pk):
    if request.method == 'POST':
        # Retrieve the form data
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        fundraising_goal = request.POST.get('fundraising_goal')

        # Update the user profile
        participant = Participant.objects.get(id=pk)
        participant.name = name
        participant.username = username
        participant.email = email
        participant.fundraising_goal = fundraising_goal
        participant.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('admin_dashboard')


def delete_user(request, pk):
    participant = Participant.objects.get(id=pk)
    participant.delete()
    return redirect('admin_dashboard')


def eventinyourcity(request):
    return render(request, 'eventinyourcity.html')


def volunteer(request):
    return render(request, 'volunteer.html')


def engagement(request):
    return render(request, 'engagement.html')

def fun(request):
    return render(request, 'fun.html')

def Web_Contact_Form_Template(request):
    return render(request, 'Web_Contact_Form_Template.html')

def homee(request):
    return render(request, 'homee.html')
