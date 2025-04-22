from rest_framework import serializers
from accounts.models import Athlete

class AthleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = ['first_name', 'last_name', 'email', 'phone', 'sex', 'age']
