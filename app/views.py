import decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import RegistrationForm  # Import the RegistrationForm
from django.contrib import messages
from django.core.mail import EmailMessage
from decimal import Decimal


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
                return redirect('admin_dashboard')
            else:
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
        # Extract the form data from the request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        zip_code = request.POST.get('zip_code')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        phone_number = request.POST.get('phone_number', '')

        # Motivations
        motivation_mental_health = 'mental_health' in request.POST.getlist('motivation')
        motivation_support_mental_health = 'support_mental_health' in request.POST.getlist('motivation')
        motivation_fight_suicide = 'fight_suicide' in request.POST.getlist('motivation')

        # Team fields
        team_option = request.POST.get('team_option', '')
        team_name = request.POST.get('team_name', '')
        is_team_captain = request.POST.get('team_captain_option', '') == 'yes'

        # Check if username already exists
        if Participant.objects.filter(username=username).exists():
            messages.error(request, 'Username already in use. Please choose another one.')
            return render(request, 'registration.html')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match. Please try again.')
            return render(request, 'registration.html')

        # Validate fundraising_goal as a decimal number
        try:
            fundraising_goal = request.POST.get('fundraising_goal')
            if fundraising_goal:  # Check if input is not empty
                fundraising_goal = decimal.Decimal(fundraising_goal)  # Convert to decimal
        except decimal.InvalidOperation:
            messages.error(request, 'Fundraising goal must be a decimal number.')
            return render(request, 'registration.html')

        # Create and save the participant record
        participant = Participant(
            username=username,
            email=email,
            password=make_password(password),  # Properly hash the password
            zip_code=zip_code,
            city=city,
            state=state,
            country=country,
            phone_number=phone_number,
            motivation_mental_health=motivation_mental_health,
            motivation_support_mental_health=motivation_support_mental_health,
            motivation_fight_suicide=motivation_fight_suicide,
            team_option=team_option,
            team_name=team_name,
            is_team_captain=is_team_captain,
            fundraising_goal=fundraising_goal if fundraising_goal else None,  # Use validated value
        )
        participant.save()

        subject = 'Successful Registration'
        content = f' Hello {username}, your registration was successful.'
        to_email = email

        email = EmailMessage(subject, content, to=[to_email])
        email.send()

        messages.success(request, 'Thank you for registering!')
        return redirect('login')  # Redirect to a new URL

    return render(request, 'registration.html')  # Change 'registration.html' to your template name


def dashboard(request):
    return render(request, 'dashboard.html')


def update_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        fundraising_goal = request.POST.get('fundraising_goal')
        team_name = request.POST.get('team_name')

        request.user.name = name
        request.user.username = username
        request.user.email = email
        request.user.fundraising_goal = fundraising_goal
        request.user.team_name = team_name
        request.user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('dashboard')


def update_account_settings(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if username and username != user.username:
            user.username = username
            user.save()
            messages.success(request, 'Username successfully updated.')
            return redirect('dashboard')

        if new_password and confirm_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password successfully updated.')
            return redirect('logout')


def admin_dashboard(request):
    participants = Participant.objects.all()
    participants_count = participants.count() - 1

    volunteers = Volunteer.objects.all()
    volunteers_count = volunteers.count() - 1

    context = {'participants': participants,
               'participants_count': participants_count,
               'volunteers': volunteers,
               'volunteers_count': volunteers_count,
               }
    return render(request, 'admin_dashboard.html', context=context)


def fetch_user_details(request, pk):
    participant = Participant.objects.get(id=pk)
    return render(request, 'fetch_user_details.html', {'participant': participant})


def update_user_detail(request, pk):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        fundraising_goal = request.POST.get('fundraising_goal')
        team_name = request.POST.get('team_name')

        participant = Participant.objects.get(id=pk)
        participant.name = name
        participant.username = username
        participant.email = email
        participant.fundraising_goal = fundraising_goal
        participant.team_name = team_name
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
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        role = request.POST.get('role')

        Volunteer.objects.create(
            full_name=full_name,
            email=email,
            role=role,
        )
        messages.success(request, f'Thank you for volunteering at the event as a {role}.')
        return redirect('volunteer')

    return render(request, 'volunteer.html')


def fetch_volunteer_details(request, pk):
    volunteer = Volunteer.objects.get(id=pk)
    return render(request, 'fetch_volunteer_details.html', {'volunteer': volunteer})


def update_volunteer_detail(request, pk):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        role = request.POST.get('role')

        volunteer = Volunteer.objects.get(id=pk)
        volunteer.full_name = full_name
        volunteer.email = email
        volunteer.role = role
        volunteer.save()

        messages.success(request, 'Volunteer updated successfully.')
        return redirect('admin_dashboard')


def delete_volunteer(request, pk):
    volunteer = Volunteer.objects.get(id=pk)
    volunteer.delete()
    return redirect('admin_dashboard')


def engagement(request):
    return render(request, 'engagement.html')


def fun(request):
    return render(request, 'fun.html')


def Web_Contact_Form_Template(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = 'Contact Form Submission'
        content = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        to_email = 'ilightproducts@gmail.com'

        email = EmailMessage(subject, content, to=[to_email])
        email.send()

        messages.success(request, 'Submitted successfully!')
        return redirect('Web_Contact_Form_Template')

    return render(request, 'Web_Contact_Form_Template.html')


def homee(request):
    return render(request, 'homee.html')


def blog1(request):
    return render(request, 'blog1.html')


def fundraise(request):
    return render(request, 'fundraise.html')


def fundraising_page(request):
    registered_teams = Participant.objects.filter(team_name__isnull=False).values_list('team_name',
                                                                                       flat=True).distinct()
    return render(request, 'fundraising.html', {'team_name': registered_teams})
