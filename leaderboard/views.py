from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Leaderboard

@api_view(["GET"])
def leaderboard(request):
    # Logic to get leaderboard
    pass
