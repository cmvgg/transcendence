from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, EmailInput, Textarea
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from django.utils import timezone
from .models import UserProfile, Tournament
from .serializers import (
    UserProfileSerializer,
    TournamentSerializer,
    TournamentResultSerializer
)

def index(request):
    return render(request, 'index.html')

def playground(request):
    return render(request, 'playground.html')

def profile(request):
    return render(request, 'profile.html')

def about(request):
    return render(request, 'about.html')

def select(request):
    return render(request, 'select.html')

def profile(request):
    return render(request, 'profile.html')

class UserProfileList(APIView):
    """
    Lista todos los perfiles de usuario o crea uno nuevo.
    """
    def get(self, request, format=None):
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y editar perfiles de usuario.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class TournamentViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y editar torneos.
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer





#def generate_players_names():
#    """    Genera nombres de jugadores de prueba.    """
#    #"Player1", "Player2", "Player3", "Player4",
#    return [
#        "Player5", "Player6", "Player7", "Player8"
#    ]

#@api_view(['POST'])

def generate_random_player_names():
    """
    Genera nombres de jugadores aleatorios.
    """
    return ["Player1", "Player2", "Player3", "Player4"]

@api_view(['POST'])
def generate_players_names(request):
    """
    Genera nombres de jugadores y crea un torneo.
    """
    try:
        # Generar nombres de jugadores
        player_names = generate_random_player_names()

        # Crear el torneo con los nombres generados
        return create_tournament(player_names)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def create_tournament(player_names):
    """
    Crea un torneo con participantes de prueba.
    """
    try:
        # Generar nombres de jugadores
        #player_names = generate_players_names()
        players = []
        for name in player_names:
            player, _ = UserProfile.objects.get_or_create(alias=name)
            players.append(player)

        # Crear el torneo
        tournament = Tournament.objects.create(name="Torneo de Prueba")
        tournament.participants.set(players)
        tournament.save()

        #"tournament_id": tournament.tournament_id,
        return Response({
            "status": "success",
            "message": f"Torneo '{tournament.name}' creado con éxito.",
            "tournament_id": 1,
            "participants": [player.alias for player in tournament.participants.all()]
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
def tournament_results(request):
    """
    Endpoint para procesar resultados de un torneo, tomando los participantes desde la base de datos.
    """
    serializer = TournamentResultSerializer(data=request.data)
    if serializer.is_valid():
        tournament_id = serializer.validated_data['tournament_id']
        results = serializer.validated_data['results']

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({
                'error': f'Tournament with ID {tournament_id} not found. Please verify the ID.'
            }, status=status.HTTP_404_NOT_FOUND)

        players = list(tournament.participants.all())
        if len(players) < 2:
            return Response({'error': 'Not enough players registered for the tournament'}, status=status.HTTP_400_BAD_REQUEST)

        for match in results:
            winner_alias = match.get('winner')
            loser_alias = match.get('loser')

            if winner_alias and loser_alias and winner_alias != "BYE" and loser_alias != "BYE":
                try:
                    winner = UserProfile.objects.get(alias=winner_alias)
                    loser = UserProfile.objects.get(alias=loser_alias)
                except UserProfile.DoesNotExist:
                    continue

                winner.wins += 1
                loser.losses += 1

                winner.save()
                loser.save()

        tournament.status = 'finished'
        tournament.save()

        return Response({
            'status': 'success',
            'tournament_id': tournament_id,
            'message': f'Resultados procesados para torneo \"{tournament.name}\"'
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_players(request):
    tournament_id = request.GET.get('tournament_id')
    
    if tournament_id:
        #players = UserProfile.objects.filter(tournaments__id=Tournament.id)  # Nota: field correcto
        try:
            tournament = Tournament.objects.get(id=tournament_id)
            players = tournament.participants.all()
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        players = UserProfile.objects.all()
    
    serializer = UserProfileSerializer(players, many=True)
    return Response(serializer.data)
class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile.objects.create(alias=user.username)
            return redirect('index')
    else:
        form = RegisterUserForm()
    return render(request, 'register.html', {'form': form})
