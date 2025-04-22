from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Workout
from django.contrib.auth.models import User

@api_view(["POST"])
def log_workout(request):
    # Logic to log a workout
    pass

@api_view(["GET"])
def workout_history(request):
    # Logic to get workout history
    pass
