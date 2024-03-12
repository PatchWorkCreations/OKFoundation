from django.db import models
from django.contrib.auth.models import AbstractUser


class Participant(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    fundraising_goal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    donation_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    team_option = models.CharField(max_length=20)
    team_name = models.CharField(max_length=255, blank=True, null=True)
    under_18 = models.BooleanField(default=False)
    mailing_address = models.TextField()
    zip_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Volunteer(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name
