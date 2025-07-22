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
from .forms import signInForm
from .models import ProfileData


def index(request):
    return render(request, 'index.html')

def playground(request):
    return render(request, 'playground.html')

def profile(request):
    #datos = UserProfileList.objects.all()  # Obtiene todos los objetos del modelo ProfileData
    #return render(request, 'profile.html', {'datos': datos})
    return render(request, 'profile.html')

def about(request):
    return render(request, 'about.html')

def select(request):
    return render(request, 'select.html')

def signIn(request):
    form_s = signInForm()
    return render(request, 'signin.html' , {'form': form_s})

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

#def register(request):
#    if request.method == 'POST':
#        form = RegisterUserForm(request.POST)
#        if form.is_valid():
#            user = form.save()
#            profile = UserProfile.objects.create(alias=user.username)
#            return redirect('index')
#    else:
#        form = RegisterUserForm()
#    return render(request, 'register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Extraer datos del formulario
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Crear el usuario utilizando el nombre como username
            user = User.objects.create_user(username=name, email=email, password=password)

            # Crear automáticamente el perfil con alias igual a name (o modificar según convenga)
            profile = UserProfile.objects.create(alias=name)
            form.save()
            # Opcional: iniciar sesión automáticamente, enviar un mensaje, redirigir, etc.
            return redirect ('http://localhost:8000/profile')  # redirige a la página de inicio, por ejemplo

    else:
        form = ExampleForm()
    return render(request, 'register.html', {'form': form})





# CUCU views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Player
import json

@login_required
#def profile_view(request):
def cucu(request):
    """Vista para mostrar la página de perfil"""
    return render(request, 'cucu.html')

@login_required
@require_http_methods(["GET"])
def get_player_data(request, player_id):
    """API endpoint para obtener datos del jugador"""
    try:
        player = get_object_or_404(Player, id=player_id)
        
        # Verificar si el usuario tiene permisos para ver este perfil
        if request.user != player.user and not request.user.is_staff:
            return JsonResponse({
                'error': 'No tienes permisos para ver este perfil'
            }, status=403)
        
        data = {
            'id': player.id,
            'nickname': player.nickname,
            'level': player.level,
            'experience': player.experience,
            'score': player.score,
            'avatar': player.avatar.url if player.avatar else None,
            'created_at': player.created_at.strftime('%Y-%m-%d'),
            'is_active': player.is_active,
            'username': player.user.username,
            'email': player.user.email,
            'first_name': player.user.first_name,
            'last_name': player.user.last_name,
        }
        
        return JsonResponse({
            'success': True,
            'player': data
        })
        
    except Player.DoesNotExist:
        return JsonResponse({
            'error': 'Jugador no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'error': f'Error interno del servidor: {str(e)}'
        }, status=500)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_player_data(request):
    """API endpoint para actualizar datos del jugador"""
    try:
        data = json.loads(request.body)
        player = get_object_or_404(Player, user=request.user)
        
        # Actualizar campos permitidos
        if 'nickname' in data:
            player.nickname = data['nickname']
        if 'level' in data:
            player.level = data['level']
        if 'experience' in data:
            player.experience = data['experience']
        if 'score' in data:
            player.score = data['score']
            
        player.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Datos actualizados correctamente'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Formato JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error al actualizar: {str(e)}'
        }, status=500)
