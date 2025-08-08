from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, EmailInput, Textarea
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import json
from django.contrib import messages

# Importar modelos y serializers
from .models import User, Tournament, Match, TournamentStats, ProfileData
from .serializers import (
    UserSerializer,
    TournamentSerializer,
    TournamentResultSerializer
)
from .forms import signInForm, ExampleForm

#variables globales
loged_user = None
loged_stats = None

def index(request):
    global loged_user, loged_stats
    return render(request, 'index.html', {'loged_user':loged_user, 'loged_stats':loged_stats})

def playground(request):
    global loged_user, loged_stats
    return render(request, 'playground.html', {'loged_user':loged_user, 'loged_stats':loged_stats})

"""@login_required
def profile(request):
	try:
        perfiles = User.objects.all().order_by('-wins', 'alias')

        total_perfiles = perfiles.count()
        total_wins = sum(p.wins for p in perfiles)
        total_losses = sum(p.losses for p in perfiles)
        total_games = total_wins + total_losses

        context = {
            'perfiles': perfiles,
            'stats': {
                'total_perfiles': total_perfiles,
                'total_wins': total_wins,
                'total_losses': total_lform
            'top_player': perfiles.first() if perfiles.exists() else None,
            # Pasamos el User y el perfil enlazado
            'user': request.user,
            'my_profile': getattr(request.user, 'profile', None),
        }
        return render(request, 'profile.html', context)

    except Exception as e:
        context = {
            'error': f'Error al cargar datos: {str(e)}',
            'perfiles': [],
            'stats': {'total_perfiles': 0, 'total_wins': 0, 'total_losses': 0, 'total_games': 0},
            'top_player': None,
            'user': request.user,
            'my_profile': getattr(request.user, 'profile', None),
        }
        return render(request, 'profile.html', context)"""
    


def about(request):
    global loged_user, loged_stats
    return render(request, 'about.html', {'loged_user':loged_user, 'loged_stats':loged_stats})

def select(request):
    global loged_user, loged_stats
    return render(request, 'select.html', {'loged_user':loged_user, 'loged_stats':loged_stats})


from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

def signIn(request):
    global loged_user, loged_stats
    if request.method == 'POST':
        form = signInForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data.get('nickname')
            passw = form.cleaned_data.get('password')
            try:
                # Intentar obtener el objeto
                usuario = User.objects.get(username=nickname)
                stats = TournamentStats.objects.get(id=usuario.id)

                # Usuario encontrado
                if check_password(passw, usuario.password):
                    loged_user = usuario
                    loged_stats = stats
                    # pass es valido
                    #return render(request, 'profile.html',{'loged_user':loged_user, 'loged_stats':loged_stats})
                    return HttpResponse("""
                         <html>
                         <head>
                            <script type="text/javascript">
                                window.opener.location.href = "/profile"
                            </script>
                            <script type="text/javascript">
                                window.close();
                            </script>
                            
                        </head>
                        <body></body>
                        </html>
                        """)
                else:
                    messages.error(request, '❌ Password incorrecto')
            except ObjectDoesNotExist:
                messages.error(request, f'El usuario {nickname} no existe')
            return HttpResponse("""
                <html>
                <head>
                    <script type="text/javascript">
                        window.close();
                    </script>
                </head>
                <body></body>
                </html>
            """)
        
    else:
        form = signInForm()
    return render(request, 'signin.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Extraer datos del formulario
            name = form.cleaned_data.get('name')
            nickname = form.cleaned_data.get('nickname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Crear el usuario utilizando el nombre como username
            user = User.objects.create_user(first_name=name, email=email, password=password, username=nickname)
            user_stats = TournamentStats.objects.create(id = user.id, username=user.username, wins=0, losses=0, tournaments_won=0)
            user_stats.save()
            # Crear el perfil de usuario
            #User.objects.create(alias=nickname, user_id=user.id)
            
            return HttpResponse("""
                <html>
                <head>
                    <script type="text/javascript">
                        window.close();
                    </script>
                </head>
                <body></body>
                </html>                                                                                                                   
            """)

    else:
        form = ExampleForm(request.GET)
    return render(request, 'register.html', {'form': form})

def editprofile(request):
    global loged_user, loged_stats
    if request.method == 'POST':


        form = ExampleForm(request.POST)
        if form.is_valid():
            # Extraer datos del formulario

            name = form.cleaned_data.get('name')
            nickname = form.cleaned_data.get('nickname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # hacer de user el usuario logeado
            user = loged_user
            user.username = nickname
            user.first_name = name
            user.email = email
            # Usar set_password para guardar la contraseña de forma segura
            user.set_password(password)
            # Guardar los cambios
            user.save()
            return HttpResponse("""
                <html>
                <head>
                    <script type="text/javascript">
                        window.close();
                    </script>
                </head>
                <body></body>
                </html>                                                                                                                   
            """)
        
    else:
        form = ExampleForm(request.GET)
    return render(request, 'editprofile.html', {'form': form, 'loged_user': loged_user})

def tournament(request):
    global loged_user, loged_stats
    return render(request, 'tournament.html', {'loged_user':loged_user, 'loged_stats':loged_stats})

# API VIEWS
class UserList(APIView):
    """Lista todos los perfiles de usuario o crea uno nuevo."""
    def get(self, request, format=None):
        user_profiles = User.objects.all()
        serializer = UserSerializer(user_profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    """API endpoint que permite ver y editar perfiles de usuario."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TournamentViewSet(viewsets.ModelViewSet):
    """API endpoint que permite ver y editar torneos."""
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

def profile_view(request):
    global loged_user, loged_stats
    #user = loged_user
    #stats = TournamentStats.objects.get(username=user.username)

    #context = {
    #    'user': user,
    #    'statistics': stats,
    #}

    return render(request, 'profile.html', {'loged_user':loged_user, 'loged_stats':loged_stats})

# API ENDPOINTS ESPECÍFICOS
@api_view(['GET'])
def get_players(request):
    """Endpoint para obtener lista de jugadores"""
    tournament_id = request.GET.get('tournament_id')
    
    if tournament_id:
        try:
            tournament = Tournament.objects.get(id=tournament_id)
            players = tournament.participants.all()
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        players = User.objects.all()
    
    serializer = UserSerializer(players, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def update_user_profile(request):
    """Actualiza las estadísticas de un jugador en la tabla api_user."""
    username = request.data.get('username')
    wins = request.data.get('wins', 0)
    losses = request.data.get('losses', 0)

    # Si no se proporciona un username, genera dos usuarios automáticamente
    if not username:
        player1, _ = User.objects.get_or_create(alias="Player1")
        player2, _ = User.objects.get_or_create(alias="Player2")
        return Response({
            'status': 'success',
            'message': 'Usuarios generados automáticamente.',
            'players': [
                {'username': player1.alias, 'wins': player1.wins, 'losses': player1.losses},
                {'username': player2.alias, 'wins': player2.wins, 'losses': player2.losses},
            ]
        }, status=status.HTTP_201_CREATED)

    # Actualizar estadísticas del usuario
    try:
        user_profile, created = User.objects.get_or_create(alias=username)
        user_profile.wins += wins
        user_profile.losses += losses
        user_profile.save()

        return Response({
            'status': 'success',
            'message': f'User for {username} updated successfully.',
            'data': {
                'username': user_profile.alias,
                'wins': user_profile.wins,
                'losses': user_profile.losses,
                'win_rate': user_profile.win_rate(),
            }
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Resto de funciones de torneo...
def generate_random_player_names_1vs1():
    """Genera nombres de jugadores aleatorios para 1vs1."""
    return ["1Player", "2Player"]

@api_view(['POST'])
def generate_players_names_1vs1(request):
    """Genera nombres de jugadores y crea un torneo."""
    try:
        player_names = generate_random_player_names_1vs1()
        return create_tournament(player_names)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def generate_random_player_names():
    """Genera nombres de jugadores aleatorios."""
    return ["Player1", "Player2", "Player3", "Player4"]

@api_view(['POST'])
def generate_players_names(request):
    """Genera nombres de jugadores y crea un torneo."""
    try:
        player_names = generate_random_player_names()
        return create_tournament(player_names)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

def create_tournament(player_names):
    """Crea un torneo con participantes de prueba."""
    try:
        players = []
        for name in player_names:
            player, _ = User.objects.get_or_create(alias=name)
            players.append(player)

        # Crear el torneo
        tournament = Tournament.objects.create(name="Torneo de Prueba")
        tournament.participants.set(players)
        tournament.save()

        return Response({
            "status": "success",
            "message": f"Torneo '{tournament.name}' creado con éxito.",
            "tournament_id": tournament.id,
            "participants": [player.alias for player in tournament.participants.all()]
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def tournament_results(request):
    """Endpoint para procesar resultados de un torneo y actualizar estadísticas."""
    serializer = TournamentResultSerializer(data=request.data)
    if serializer.is_valid():
        tournament_id = serializer.validated_data['tournament_id']
        results = serializer.validated_data['results']
        tournament_winner_alias = serializer.validated_data.get('winner')

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({
                'error': f'Tournament with ID {tournament_id} not found. Please verify the ID.'
            }, status=status.HTTP_404_NOT_FOUND)

        players = list(tournament.participants.all())
        if len(players) < 4:
            return Response({'error': 'Not enough players registered for the tournament'}, status=status.HTTP_400_BAD_REQUEST)

        # Procesar resultados del torneo
        for match in results:
            winner_alias = match.get('winner')
            loser_alias = match.get('loser')

            if winner_alias and loser_alias and winner_alias != "BYE" and loser_alias != "BYE":
                try:
                    winner = User.objects.get(alias=winner_alias)
                    loser = User.objects.get(alias=loser_alias)
                except User.DoesNotExist:
                    print(f"Alias no encontrado: winner={winner_alias}, loser={loser_alias}")
                    continue

                # Actualizar estadísticas de los jugadores
                winner.wins += 1
                loser.losses += 1
                winner.save()
                loser.save()

        # Actualizar el ganador del torneo
        if tournament_winner_alias:
            try:
                tournament_winner = User.objects.get(alias=tournament_winner_alias)
                tournament.winner = tournament_winner
                tournament.status = 'finished'
                tournament.save()
            except User.DoesNotExist:
                return Response({'error': f'Winner alias "{tournament_winner_alias}" not found.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'status': 'success',
            'tournament_id': tournament_id,
            'message': f'Resultados procesados para torneo "{tournament.name}". Ganador: {tournament_winner_alias}'
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_players(request):
    tournament_id = request.GET.get('tournament_id')
    
    if tournament_id:
        #players = User.objects.filter(tournaments__id=Tournament.id)  # Nota: field correcto
        try:
            tournament = Tournament.objects.get(id=tournament_id)
            players = tournament.participants.all()
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        players = User.objects.all()
    
    serializer = UserSerializer(players, many=True)
    return Response(serializer.data)
class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



