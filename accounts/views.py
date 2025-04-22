from django.shortcuts import render
from accounts.models import Athlete
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import HttpResponse, get_object_or_404
from django.contrib.auth.models import User
import logging
from rest_framework.response import Response
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout as auth_logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializers import AthleteSerializer

# Create your views here.

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    Accepts json data from frontend to allow user
    to register based on needed fields.
    """
    
    # do not create new user if user is already logged in
    if request.user.is_authenticated:
        refresh = RefreshToken.for_user(request.user)
        return HttpResponse(f"{request.user.username, refresh} is logged in already")
    else:
        if request.method == "POST":
            data = request.data
            try:
                new_athlete = Athlete.objects.create(
                    first_name=data.get("first_name", None),
                    last_name=data.get("last_name", None),
                    email=data.get("email", None),
                    phone=data.get("phone", None),
                    username=data.get("username", None),
                    sex=data.get("sex", None),
                    age=data.get("age", None),
                )
                new_athlete.save()

                

                # create user based on athlete to leverage built in django.contrib.auth.models
                user_match = User.objects.create_user(
                    first_name=data.get("first_name", None),
                    last_name=data.get("last_name", None),
                    username=data.get("username", None),
                    password=data.get("password", None),
                    email=data.get("email", None),
                )
                user_match.save()
                return Response({"athlete": new_athlete.username})
            
            # error checking for if user already exist based on username constraint
            except IntegrityError as e:
                nullness_error = "NOT NULL constraint failed: "
                if nullness_error in str(e) and "username" in str(e):
                    return Response(data={"reason": "Username already exists"})
                else:
                    return Response(data={"reason": str(e)})
            except Exception as e:
                logging.exception("Error")
                return Response(data={"reason": str(e)})

@api_view(["GET"])
@permission_classes([AllowAny])
def current_user_data(request):
    """
    Generates refresh token for user and provides
    important user information for the front end.
    """
    response = Response()

    user_record = User.objects.get(username=request.user.username)

    if not user_record:
        logging.debug(f"User does not exist: {request.user.username}")
        return None

    refresh = RefreshToken.for_user(user_record)
    csrf_token = get_token(request)

    # for some reason this correctly converts the refresh dict to a token string
    response["refresh-token"] = refresh

    logging.info(f"Logged in: {user_record.username}")

    return {
        "auth": {"refresh": response["refresh-token"], "csrf": csrf_token},
        "user": {
            "first_name": user_record.first_name,
            "last_name": user_record.last_name,
            "username": user_record.username,
        },

    }

@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def sign_in(request):

    if request.user.is_authenticated:
        refresh = RefreshToken.for_user(request.user)
        return Response(f"{request.user.username, refresh} is logged in already")
    else:
        if request.method == "POST":
            data = request.data
            username = data["username"]
            password = data["password"]
            if not username or not password:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={"reason": "Username and password are required."},
                )

            user_record = None
            try:
                user_record = User.objects.get(username=username)
            except User.DoesNotExist:
                if str(username[0]).upper():
                    username = str(username[0]).lower() + str(username[1:])
                    try:
                        user_record = User.objects.get(username=username)
                    except User.DoesNotExist:
                        pass

            # Authenticate the user
            if user_record:
                auth_user = authenticate(
                    request=request, username=username, password=password
                )
                if auth_user:
                    login(request, user_record)
                    return Response(current_user_data(request))

            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={"reason": "Invalid login credentials."},
            )
@csrf_exempt
@api_view(["GET"])
@permission_classes([AllowAny])
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return Response({"message": "Logged out"}, status=200)

@csrf_exempt
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    try:
        athlete = Athlete.objects.get(username=request.user.username)
    except Athlete.DoesNotExist:
        return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AthleteSerializer(athlete, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Profile updated successfully.",
            "profile": serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)