from django import forms
from .models import Participant

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    zip_code = forms.CharField(max_length=10)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=20, required=False)
    fundraising_goal = forms.DecimalField(max_digits=10, decimal_places=2)
    team_name = forms.CharField(max_length=100)

class AddMemberForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'username']  # Add 'username' field here


from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']  # Adjust the fields as per your Donation model


from .models import Sponsorship

class SponsorshipForm(forms.ModelForm):
    class Meta:
        model = Sponsorship
        fields = ['name', 'company', 'email', 'website_link', 'level', 'donation_amount']
