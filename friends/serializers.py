from rest_framework import serializers
from .models import Friendship
from django.contrib.auth import get_user_model

class FriendshipSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    friend = serializers.StringRelatedField()
    
    class Meta:
        model = Friendship
        fields = ['user', 'friend', 'status']
