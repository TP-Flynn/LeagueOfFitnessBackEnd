from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Profile
from django.contrib.auth.models import User

@api_view(["GET"])
def view_profile(request):
    # Logic to view a user profile
    pass

@api_view(["POST"])
def edit_profile(request):
    # Logic to edit user profile
    pass
