from rest_framework import serializers
from .models import UserProfile, Tournament

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'alias', 'wins', 'losses']

class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'start_date']

class MatchResultSerializer(serializers.Serializer):
    winner = serializers.CharField()
    loser = serializers.CharField()

class TournamentResultSerializer(serializers.Serializer):
    tournament_id = serializers.IntegerField()
    results = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    winner = serializers.CharField()

