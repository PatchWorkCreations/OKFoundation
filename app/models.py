from django.db import models
from django.contrib.auth.models import AbstractUser


class Participant(AbstractUser):
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

    def __str__(self):
        # Return the participant's full name
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username


class Volunteer(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name
