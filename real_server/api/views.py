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
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Importar modelos y serializers
from .models import User, Tournament, Match, TournamentStats, ProfileData, UserProfile
from .serializers import (
    UserSerializer,
    TournamentSerializer,
    TournamentResultSerializer
)
# import the forms: sign in and register 
from .forms import signInForm, RegisterForm

#variables globales
loged_user = None
loged_stats = None

def index(request):
    global loged_user, loged_stats
    return render(request, 'index.html', {'loged_user':loged_user, 'loged_stats':loged_stats})

def playground(request):
    top = TournamentStats.objects.order_by('wins').last()
    user = request.user
    profile = UserProfile.objects.get(user = user)
    return render(request, 'playground.html', {'loged_user':user, 'high_score': top, 'profile': profile})
 
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

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

def signIn(request): #login
    if request.method == 'POST':
        form = signInForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data.get('nickname')
            passw = form.cleaned_data.get('password')
            user = authenticate(request, username=nickname, password=passw)
            if user is not None:
                login(request, user)
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
        form = signInForm()
    return render(request, 'signin.html', {'form': form})

from django.contrib.auth import logout
def logout_view(request):
    #username = UserLoggedIn(request)
    user = User
    if user != None:
        logout(request)
        return redirect("/")

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Extraer datos del formulario
            name = form.cleaned_data.get('name')
            nickname = form.cleaned_data.get('nickname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            avatar = form.cleaned_data.get('avatar')
            if User.objects.filter(username=nickname).exists():
                    messages.error(request, 'This username already exists.')
            else:
                    # Crear el usuario utilizando el nombre como username
                    user = User.objects.create_user(first_name=name, email=email, password=password, username=nickname)
                    login(request, user)
                    profile = UserProfile.objects.get(user = user)
                    profile.avatar = avatar
                    profile.save()
                    # Crear estadisticas de usuario
                    user_stats = TournamentStats.objects.create(id = user.id, username=user.username, wins=0, losses=0, tournaments_won=0)
                    user_stats.save()
                    # Crear el perfil de usuario
                    #user_profile = UserProfile.objects.create(
                    #    user = user,
                    #    avatar= avatar,
                    #)
                    #user_profile.friends.add(user.id)
                    #user_profile.save()
                    
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
        form = RegisterForm(request.GET)
    return render(request, 'register.html', {'form': form})

def editprofile(request):
    global loged_user, loged_stats
    if request.method == 'POST':


        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Extraer datos del formulario
            name = form.cleaned_data.get('name')
            nickname = form.cleaned_data.get('nickname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            avatar = form.cleaned_data.get('avatar')

            # hacer de user el usuario logeado
            #user = User.objects.get(username=nickname)
            user = request.user
            stats = TournamentStats.objects.get(user=user)
            user.set_password(password)
            user.username = nickname
            user.first_name = name
            user.email = email
            user.UserProfile.avatar = avatar
            
            # Guardar los cambios
            user.save()
            user.UserProfile.save()
            login(request, user)
            log_user = authenticate(request, username=nickname, password=password)
            stats = TournamentStats.objects.get(user=log_user)
            #return render(request, 'signin.html', {'form': form})
            return redirect("profile.html", {'log_user': log_user, 'loged_stats':stats})
        
    else:
        form = RegisterForm(request.GET, request.FILES)
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
    logedUser = request.user #the active or loged user, the one who makes de request
    username = logedUser.username
    profile = UserProfile.objects.get(user = logedUser)

    if request.user.is_authenticated:
        logedUser = request.user
        profile = UserProfile.objects.get(user = logedUser)
        friends_usernames = User.objects.filter(id__in=profile.friends).values_list('username', flat=True)
        friends_online = UserProfile.objects.filter(id__in=profile.friends).values_list('is_online', 'user')
        cucus = User.objects.filter(id__in=profile.friends)
    return render(request, 'profile.html', {'profile': profile, 'friends_names': friends_usernames, 'friends_online': friends_online, 'cucus': cucus})

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

#user friends
from django.contrib.auth import get_user_model # Importa el modelo de usuario actual

User = get_user_model() # Obtiene el modelo de usuario

def lista_y_selecciona_usuarios(request):
    if request.method == 'POST':
        # Manejar los datos del formulario si se seleccionaron usuarios
        usuarios_seleccionados_ids = request.POST.getlist('usuarios') # Obtener IDs de los usuarios seleccionados
        usuarios_seleccionados = User.objects.filter(id__in=usuarios_seleccionados_ids)

        # guardar los usuarios seleccionados como amigos del usuario activo
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
        
        #user_profile.friends = usuarios_seleccionados_ids
        for usuario in usuarios_seleccionados:
            if usuario != user:
                user_profile.friends.append(usuario.id)
                mutual = UserProfile.objects.get(user=usuario)
                mutual.friends.append(user.id)
        user_profile.save()
        mutual.save()

        # Opcional: Redirigir después del procesamiento
        # from django.shortcuts import redirect
        # return redirect('ruta_a_otra_pagina')

        context = {'usuarios_seleccionados': usuarios_seleccionados}
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
        # Si es un GET, muestra la lista para seleccionar
        usuarios = User.objects.all()
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
        usuarios = User.objects.all().exclude(id__in=user_profile.friends)
        context = {'usuarios': usuarios}
        return render(request, 'lista_usuarios.html', context)


def delete_friends(request):
    if request.method == 'POST':
        # form data management
        usuarios_seleccionados_ids = request.POST.getlist('usuarios') # get IDs from selected users
        usuarios_seleccionados = User.objects.filter(id__in=usuarios_seleccionados_ids)

        # active user and its profile
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
        #remove selection from userprofile friends
        for usuario in usuarios_seleccionados:
            if usuario != user:
                user_profile.friends.remove(usuario.id)
                mutual = UserProfile.objects.get(user=usuario)
                mutual.friends.remove(user.id)
        user_profile.save()
        mutual.save()

        context = {'usuarios_seleccionados': usuarios_seleccionados}
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
        # in case it is a GET, show friends list to choose
        #usuarios = User.objects.all() #¿necesaria esta linea?
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
        usuarios = User.objects.filter(id__in=user_profile.friends)
        context = {'usuarios': usuarios}
        return render(request, 'delete_friends.html', context)

#user friends END

