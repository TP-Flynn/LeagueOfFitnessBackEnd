from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# Custom User Manager
class AthleteManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

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
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    sex = models.CharField(choices=sex_choices, null=True, blank=True, max_length=7)
    age = models.IntegerField(default=0, null=True, blank=True)
    leaderboard_points = models.IntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = AthleteManager()

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True    