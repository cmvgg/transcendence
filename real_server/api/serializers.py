from rest_framework import serializers
from .models import UserProfile, Tournament

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'alias', 'wins', 'losses']

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'start_date']

class TournamentResultSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    results = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField(required=False),
        )
    )