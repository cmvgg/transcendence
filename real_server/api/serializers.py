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
    """ def validate_results(self, value):
        for match in value:
            winner = match.get('winner')
            loser = match.get('loser')
            if winner and winner != "BYE" and not UserProfile.objects.filter(alias=winner).exists():
                raise serializers.ValidationError(f"Winner alias '{winner}' does not exist.")
            if loser and loser != "BYE" and not UserProfile.objects.filter(alias=loser).exists():
                raise serializers.ValidationError(f"Loser alias '{loser}' does not exist.")
        return value """
