from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tournament, UserProfile
from .serializers import TournamentResultSerializer

class TournamentResultView(APIView):
    def post(self, request):
        serializer = TournamentResultSerializer(data=request.data)
        if serializer.is_valid():
            tournament_id = serializer.validated_data['tournament_id']
            results = serializer.validated_data['results']

            try:
                tournament = Tournament.objects.get(id=tournament_id)
            except Tournament.DoesNotExist:
                return Response({'error': 'Tournament not found.'}, status=status.HTTP_404_NOT_FOUND)

            for match in results:
                winner_alias = match.get('winner')
                loser_alias = match.get('loser')

                try:
                    winner = UserProfile.objects.get(alias=winner_alias)
                    loser = UserProfile.objects.get(alias=loser_alias)
                except UserProfile.DoesNotExist:
                    return Response({'error': f"Invalid alias: {winner_alias} or {loser_alias}"}, status=status.HTTP_400_BAD_REQUEST)

                winner.wins += 1
                loser.losses += 1

                winner.save()
                loser.save()

            tournament.status = 'finished'
            tournament.save()

            return Response({'message': 'Tournament results processed successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)