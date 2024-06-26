import decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import RegistrationForm  # Import the RegistrationForm
from django.contrib import messages
from django.core.mail import EmailMessage
from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from django.db.models import Q


from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Participant, Volunteer

def schedule_call(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        country = request.POST.get('country')

        # Process the data, save it to the database, or send an email
        subject = 'Schedule a Call Submission'
        content = f'Name: {name}\nEmail: {email}\nPhone: {phone}\nCity: {city}\nCountry: {country}'
        to_email = 'officialpatchwork07@gmail.com'

        email_message = EmailMessage(subject, content, to=[to_email])
        email_message.send()

        messages.success(request, 'We have received your submission. Thank you for supporting our cause!')
        return JsonResponse({'message': 'Success'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def contact_form_submission(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Process the data, save it to the database, or send an email
        subject = 'Contact Form Submission'
        content = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        to_email = 'officialpatchwork07@gmail.com'  # Your target email address

        email_message = EmailMessage(subject, content, to=[to_email])
        email_message.send()

        messages.success(request, 'We have received your submission. Thank you for supporting our cause!')
        return JsonResponse({'message': 'Success'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def generate_csv(request):
    participants = Participant.objects.all()  # Assuming Participant is your model name
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="participants.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Date Registered', 'Team Name', 'Fundraising Goal'])

    for participant in participants:
        writer.writerow([participant.name, participant.email, participant.created, participant.team_name, participant.fundraising_goal])

    return response


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
    participants = Participant.objects.all()
    # Generate a set of unique, non-empty team names
    unique_team_names = {participant.team_name for participant in participants if
                         participant.team_name and participant.team_name.strip()}

    if request.method == 'POST':
        # Extract the form data from the request
        name = request.POST.get('name')
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
        is_team_captain = request.POST.get('team_captain_option', '') == 'yes'
        team_option = request.POST.get('team_option', '')
        if team_option == 'start_team':
            team_name = request.POST.get('new_team_name', '')
        elif team_option == 'join_team':
            team_name = request.POST.get('existing_team_name', '')
        else:
            team_name = None  # No team name for solo participants

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
            name=name,
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
        content = f' Hello {name}, your registration was successful.'
        to_email = email

        email = EmailMessage(subject, content, to=[to_email])
        email.send()

        messages.success(request, 'Thank you for registering!')
        return redirect('login')  # Redirect to a new URL

    return render(request, 'registration.html', {'unique_team_names': unique_team_names})


def dashboard(request):
    # Check if the user is a team captain
    if request.user.is_team_captain:
        # Get all members of the user's team
        team_members = Participant.objects.filter(team_name=request.user.team_name).exclude(id=request.user.id)
    else:
        team_members = []

    context = {
        'team_members': team_members,
    }
    return render(request, 'dashboard.html', context)


def update_user(request):
    def update_user(request):
   
     if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        fundraising_goal = request.POST.get('fundraising_goal')
        team_name = request.POST.get('team_name')

        # Set fundraising_goal to 0 if it's None
        if fundraising_goal is None:
            fundraising_goal = 0

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
        team_option = request.POST.get('team_option', 'participate_solo')  # Default to 'participate_solo'
        team_name = request.POST.get('team_name', '')  # Get the team name, if provided

        user = request.user

        # Update username
        if username and username != user.username:
            user.username = username

        # Update password
        if new_password and confirm_password and new_password == confirm_password:
            user.set_password(new_password)

        # Handle team options
        if team_option == 'start_team' or team_option == 'join_team':
            user.team_name = team_name
            user.team_option = team_option
            # Set the user as a team captain if they chose to start a team
            user.is_team_captain = team_option == 'start_team'

        user.save()

        messages.success(request, 'Account settings updated successfully.')
        return redirect('dashboard')


from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.http import JsonResponse
from django.db import connection
from .models import Participant, Volunteer, Donation
import logging

logger = logging.getLogger(__name__)

def admin_dashboard(request):
    try:
        participants = Participant.objects.all()
        participants_count = participants.count() - 1

        volunteers = Volunteer.objects.all()
        volunteers_count = volunteers.count() - 1

        # Check if the sort_by query parameter exists in the request
        sort_by = request.GET.get('sort_by')

        # Sort participants by team option if the query parameter exists
        if sort_by == 'team_option':
            participants = participants.order_by('team_option')

        # Fetch donations for each participant
        for participant in participants:
            donation = Donation.objects.filter(participant=participant).aggregate(total_amount=Sum('amount'))
            participant.donation = donation['total_amount'] if donation['total_amount'] else 'N/A'

        context = {
            'participants': participants,
            'participants_count': participants_count,
            'volunteers': volunteers,
            'volunteers_count': volunteers_count,
        }
        return render(request, 'admin_dashboard.html', context=context)
    except Exception as e:
        logger.error("Error in admin_dashboard view: %s", str(e))
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        # Close any open database connections to prevent connection leaks
        connection.close()

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
        return redirect('dashboard')


def delete_user(request, pk):
    participant = Participant.objects.get(id=pk)
    participant.delete()

    # Check if the current user is an admin or a team captain
    if request.user.is_superuser:
        # Admin is deleting, redirect to admin dashboard
        return redirect('admin_dashboard')
    else:
        # Team captain is deleting, redirect to dashboard
        return redirect('dashboard')


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


def fundraising_page(request):
    registered_teams = Participant.objects.filter(team_name__isnull=False).values_list('team_name',
                                                                                       flat=True).distinct()
    return render(request, 'fundraising.html', {'team_name': registered_teams})


def fundraise(request):
    # Retrieve all registered teams along with their total fundraising goals
    registered_teams = Participant.objects.exclude(team_name__in=[None, '']).values('team_name').annotate(
        total_fundraising_goal=Sum('fundraising_goal')).order_by('team_name')

    # Retrieve solo participants or participants with team_option set to "participating solo"
    solo_participants = Participant.objects.filter(
        Q(team_option='participating solo') | Q(team_option='participate_solo') | Q(team_name__isnull=True),
        fundraising_goal__isnull=False
    ).values('name', 'fundraising_goal')

    context = {
        'registered_teams': registered_teams,
        'solo_participants': solo_participants,
    }

    return render(request, 'fundraise.html', context)

def team_detail(request, team_name):
    # Retrieve all participants for the team
    participants = Participant.objects.filter(team_name=team_name)

    # Find the team captain
    team_captain = participants.filter(is_team_captain=True).first()

    # Calculate the total fundraising goal for the team captain
    captain_fundraising_goal = participants.filter(is_team_captain=True).aggregate(total_goal=Sum('fundraising_goal'))['total_goal']

    # Calculate the total donation amount for the team
    total_donation = Donation.objects.filter(participant__team_name=team_name).aggregate(total_amount=Sum('amount'))['total_amount']

    # Calculate the fundraising progress as a percentage
    captain_fundraising_progress = Donation.objects.filter(participant=team_captain).aggregate(total_amount=Sum('amount'))['total_amount'] if team_captain else 0
    captain_fundraising_progress_percentage = (captain_fundraising_progress / captain_fundraising_goal) * 100 if captain_fundraising_goal else 0

    # Pass the team captain, participants, total fundraising goal, and total donation to the template
    context = {
        'team_name': team_name,
        'team_captain': team_captain,
        'participants': participants,
        'captain_fundraising_goal': captain_fundraising_goal,
        'total_donation': total_donation,
        'captain_fundraising_progress': captain_fundraising_progress,
        'captain_fundraising_progress_percentage': captain_fundraising_progress_percentage
    }
    return render(request, 'team_detail.html', context)



def sponsors(request):
    return render(request, 'sponsors.html')

from .forms import AddMemberForm
@login_required
def add_member(request):
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            
            # Set team name as the team captain's team
            team_name = request.user.team_name
            
            # Create new member
            member = Participant(
                name=name,
                email=email,
                username=username,
                team_name=team_name,
                is_team_captain=False,  # Ensure added member is not marked as team captain
            )
            member.save()
            
            messages.success(request, 'Member added successfully.')
            return redirect('dashboard')  # Redirect to the dashboard after successful form submission
        else:
            messages.error(request, 'Failed to add member. Please check the form.')
    else:
        form = AddMemberForm()
    return render(request, 'dashboard.html', {'form': form})

from django.http import HttpResponse
from .models import Participant, Donation
from .forms import DonationForm


from .models import Participant, Donation
from .forms import DonationForm
def edit_donation(request, username):
    participant = get_object_or_404(Participant, username=username)
    donation = Donation.objects.filter(participant=participant).first()

    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.participant = participant
            donation.save()
            print(f"Donation updated: {donation.amount}")  # Debugging print statement
            return redirect('admin_dashboard')
        else:
            print("Form is not valid")  # Debugging print statement
    else:
        form = DonationForm(instance=donation)

    return render(request, 'edit_donation.html', {'form': form})

from .forms import SponsorshipForm

def sponsorship_form(request):
    if request.method == 'POST':
        form = SponsorshipForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'sponsors.html', {'form': form, 'submitted': True})  # Set 'submitted' to True
    else:
        form = SponsorshipForm()
    return render(request, 'sponsors.html', {'form': form, 'submitted': False})

def teamcaptainfactsheet(request):
    return render(request, 'teamcaptainfactsheet.html')

def Registration_2(request):
    return render(request, 'Registration_2.html')

