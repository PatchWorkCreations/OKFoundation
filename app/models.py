from django.db import models
from django.contrib.auth.models import AbstractUser


class Participant(AbstractUser):
    name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Additional fields specific to your application
    motivation_mental_health = models.BooleanField(default=False)
    motivation_support_mental_health = models.BooleanField(default=False)
    motivation_fight_suicide = models.BooleanField(default=False)
    team_option = models.CharField(max_length=50, blank=True, null=True)
    team_name = models.CharField(max_length=100, blank=True, null=True)
    is_team_captain = models.BooleanField(default=False)
    fundraising_goal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    donation_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Donation(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Donation by {self.participant.name} - ${self.amount}"


class Volunteer(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class SponsorshipLevel(models.Model):
    LEVEL_CHOICES = [
        ('bronze', 'Bronze Community Supporter'),
        ('silver', 'Silver Hope Advocate'),
        ('gold', 'Gold Lifesaver Leader'),
        ('platinum', 'Platinum Empathy Champion'),
        ('titanium', 'Titanium Community Ambassador'),
    ]
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)

class Sponsorship(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, default="NA")
    email = models.EmailField()
    website_link = models.URLField(blank=True, null=True)  # Optional field for website link or page link
    level = models.ForeignKey(SponsorshipLevel, on_delete=models.CASCADE)  # ForeignKey relationship with SponsorshipLevel
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Nullable field for donation amount
    price = models.CharField(max_length=20)
    details = models.TextField()