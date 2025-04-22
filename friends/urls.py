from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_friend, name='add_friend'),
    path('remove/', views.remove_friend, name='remove_friend'),
    path('list/', views.list_friends, name='list_friends'),
]
