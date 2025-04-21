from django.db import models

# Create your models here.

class Athlete(AbstractBaseUser):
    sex_choices = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    USERNAME_FIELD = "username"
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    username = models.CharField(max_length=40, blank=False, unique=True)
    email = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    sex = models.CharField(choices=sex_choices, null=True, blank=True, max_length=7)
    age = models.IntegerField(default=0, null=True, blank=True)
    leaderboard_points = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.username}"    