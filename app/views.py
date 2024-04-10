from django.contrib.auth import authenticate, login, logout
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
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            zip_code = form.cleaned_data['zip_code']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            phone_number = form.cleaned_data['phone_number']
            fundraising_goal = form.cleaned_data['fundraising_goal']
            team_name = form.cleaned_data['team_name']

            if password == confirm_password:
                if Participant.objects.filter(username=username).exists():
                    messages.warning(request, 'Username is already taken. Please choose another.')
                else:
                    Participant.objects.create_user(
                        name=name,
                        email=email,
                        username=username,
                        password=password,
                        zip_code=zip_code,
                        city=city,
                        state=state,
                        phone_number=phone_number,
                        fundraising_goal=fundraising_goal,
                        team_name=team_name  # Save team_name here
                    )

                    subject = 'Successful Registration'
                    content = f' Hello {name}, your registration was successful.'
                    to_email = email

                    email = EmailMessage(subject, content, to=[to_email])
                    email.send()

                    messages.success(request, 'Registration successful. You can now log in.')
                    return redirect('login')
            else:
                messages.warning(request, 'Passwords did not match. Please try again.')
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})

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
    registered_teams = Participant.objects.filter(team_name__isnull=False).values_list('team_name', flat=True).distinct()
    return render(request, 'fundraising.html', {'team_name': registered_teams})

