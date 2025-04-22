from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log_workout, name='log_workout'),
    path('history/', views.workout_history, name='workout_history'),
]
