from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.sign_in),
    path("logout/", views.logout),
    path("update-profile/", views.update_profile),
]
