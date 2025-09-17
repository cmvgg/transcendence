from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Tournament, UsersInTournament, UserProfile
# Importar modelos y serializers
import json
from django.contrib.auth import authenticate, login
# Importar modelos y serializers
from .serializers import (
    UserSerializer,
    TournamentSerializer,
)
# import the forms: sign in and register 
from .forms import signInForm, RegisterForm, EditProfileForm

loged_user = None
loged_stats = None

from django.shortcuts import redirect
def index(request):
    global loged_user, loged_stats
    return render(request, 'index.html', {'loged_user':loged_user, 'loged_stats':loged_stats})

def playground(request):
    global loged_user, loged_stats
    users_in_tournament = UsersInTournament.objects.all()
    if users_in_tournament.count() < 2:
        users_in_tournament.delete()
        return render(request, 'error.html', {
            'message': "No hay suficientes usuarios para jugar 1vs1.",
            'redirect_url': 'select',
            'redirect_text': 'Volver'
        })
    top = UserProfile.objects.order_by('wins').last()
    return render(request, 'playground.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'high_score': top})

def playground2(request):
    global loged_user, loged_stats
    if not request.user.is_authenticated:
        return render(request, 'error.html', {
            'message': "Your are not logged in to play 1vsIA.",
            'redirect_url': 'select',
            'redirect_text': 'Volver'
        })
    top = UserProfile.objects.order_by('wins').last()
    return render(request, 'playground_copy.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'high_score': top})

def battleground(request):
    global loged_user, loged_stats
    users_in_tournament = UsersInTournament.objects.all()
    if users_in_tournament.count() < 4:
        users_in_tournament.delete()
        return render(request, 'error.html', {
            'message': "No hay suficientes usuarios para jugar battleground (mínimo 4).",
            'redirect_url': 'select',
            'redirect_text': 'Volver'
        })
    top = UserProfile.objects.order_by('wins').last()
    return render(request, 'battleground.html', {'loged_user':loged_user, 'loged_stats':loged_stats, 'high_score': top})

def tron(request):
    global loged_user, loged_stats
    users_in_tournament = UsersInTournament.objects.all()
    if users_in_tournament.count() < 2:
        users_in_tournament.delete()
        return render(request, 'error.html', {
            'message': "No hay suficientes usuarios para jugar tron.",
            'redirect_url': 'select',
            'redirect_text': 'Volver'
        })
    top = UserProfile.objects.order_by('wins').last()
    return render(request, 'playground_tron.html', {'loged_user':loged_user, 'loged_stats':loged_stats, 'high_score': top})

def tournament(request):
    global loged_user, loged_stats
    users_in_tournament = UsersInTournament.objects.all()
    if users_in_tournament.count() < 4:
        users_in_tournament.delete()
        return render(request, 'error.html', {
            'message': "No hay suficientes usuarios para un torneo (mínimo 4).",
            'redirect_url': 'select',
            'redirect_text': 'Volver'
        })
    top = UserProfile.objects.order_by('wins').last()
    return render(request, 'tournament.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'high_score': top})

def about(request):
    global loged_user, loged_stats
    return render(request, 'about.html', {'loged_user':loged_user, 'loged_stats':loged_stats})

def select(request):
    global loged_user, loged_stats
    return render(request, 'select.html', {'loged_user':loged_user, 'loged_stats':loged_stats})

from django.shortcuts import get_object_or_404
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

import django.contrib.messages as messages
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

def tmp1vs1(request):
    global loged_user, loged_stats
    usuarios = list(UserProfile.objects.filter(is_online=True))
    current_user = request.user
    usuarios.sort(key=lambda u: u.user.id != current_user.id)
    if not request.user.is_authenticated:
        return render(request, 'error.html', {
            'message': "You are not logued in.",
            'redirect_url': 'select',
            'redirect_text': 'Log in'
        })
    return render(request, '1vs1_waitlist.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'usuarios': usuarios, 'current_user': current_user})

def tmpbattleground(request):
    global loged_user, loged_stats
    usuarios = list(UserProfile.objects.filter(is_online=True))
    current_user = request.user
    usuarios.sort(key=lambda u: u.user.id != current_user.id)
    if not request.user.is_authenticated:
        return render(request, 'error.html', {
            'message': "You are not logued in.",
            'redirect_url': 'select',
            'redirect_text': 'Log in'
        })
    return render(request, 'battleground_waitlist.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'usuarios': usuarios, 'current_user': current_user})

def tmptron(request):
    global loged_user, loged_stats
    usuarios = list(UserProfile.objects.filter(is_online=True))
    current_user = request.user
    usuarios.sort(key=lambda u: u.user.id != current_user.id)
    if not request.user.is_authenticated:
        return render(request, 'error.html', {
            'message': "You are not logued in.",
            'redirect_url': 'select',
            'redirect_text': 'Log in'
        })
    return render(request, 'tron_waitlist.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'usuarios': usuarios, 'current_user': current_user})

def tmptournament(request):
    global loged_user, loged_stats
    usuarios = list(UserProfile.objects.filter(is_online=True))
    current_user = request.user
    usuarios.sort(key=lambda u: u.user.id != current_user.id)
    if not request.user.is_authenticated:
        return render(request, 'error.html', {
            'message': "You are not logued in.",
            'redirect_url': 'select',
            'redirect_text': 'Log in'
        })
    return render(request, 'tournament_waitlist.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'usuarios': usuarios, 'current_user': current_user})

@csrf_exempt
def duplicate_1vsIA(request):
    if request.method == 'POST':
        try:
            UsersInTournament.objects.all().delete()
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User not autenticated.'}, status=401)
            player = UserProfile.objects.get(user=request.user)
            UsersInTournament.objects.create(
                username=player.user.username,
                wins=player.wins,
                losses=player.losses,
                tournaments_won=player.tournaments_won
            )
            return JsonResponse({'redirect_url': '/playground2'}, status=200)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'El usuario logueado no tiene un perfil asociado.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@csrf_exempt
def duplicate_1vs1(request):
    if request.method == 'POST':
        try:
            selected_player_ids = request.POST.getlist('player_ids[]')
            if not selected_player_ids or len(selected_player_ids) != 2:
                return JsonResponse({'error': 'Se necesitan exactamente 2 jugadores para 1vs1.'}, status=400)
            UsersInTournament.objects.all().delete()
            for player_id in selected_player_ids:
                player = UserProfile.objects.get(user_id=player_id)
                UsersInTournament.objects.create(
                    username=player.user.username,
                    wins=0,
                    losses=0,
                    tournaments_won=0
                )
            return redirect('playground')
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Uno o más jugadores no existen.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@csrf_exempt
def duplicate_battleground(request):
    if request.method == 'POST':
        try:
            selected_player_ids = request.POST.getlist('player_ids[]')
            if not selected_player_ids or len(selected_player_ids) < 4:
                return JsonResponse({'error': 'Se necesitan al menos 4 jugadores para jugar.'}, status=400)
            UsersInTournament.objects.all().delete()
            for player_id in selected_player_ids:
                player = UserProfile.objects.get(user_id=player_id)
                UsersInTournament.objects.create(
                    username=player.user.username,
                    wins=0,
                    losses=0,
                    tournaments_won=0 
                )
            return redirect('battleground')
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Uno o más jugadores no existen.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@csrf_exempt
def duplicate_tron(request):
    if request.method == 'POST':
        try:
            selected_player_ids = request.POST.getlist('player_ids[]')
            if not selected_player_ids or len(selected_player_ids) < 2:
                return JsonResponse({'error': 'Se necesitan al menos 2 jugadores para jugar.'}, status=400)
            UsersInTournament.objects.all().delete()
            for player_id in selected_player_ids:
                player = UserProfile.objects.get(user_id=player_id)
                UsersInTournament.objects.create(
                    username=player.user.username,
                    wins=0,
                    losses=0,
                    tournaments_won=0 
                )
            return redirect('tron')
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Uno o más jugadores no existen.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

from math import log2
@csrf_exempt
def duplicate_tournament(request):
    if request.method == 'POST':
        try:
            selected_player_ids = request.POST.getlist('player_ids[]')
            if not selected_player_ids or len(selected_player_ids) < 4:
                return JsonResponse({'error': 'Se necesitan al menos 4 jugadores para un torneo.'}, status=400)
            if log2(len(selected_player_ids)) % 1 != 0:
                return JsonResponse({'error': 'El número de jugadores debe ser una potencia de 2 (4, 8, 16, 32, etc.).'}, status=400)
            UsersInTournament.objects.all().delete()
            for player_id in selected_player_ids:
                player = UserProfile.objects.get(user_id=player_id)
                UsersInTournament.objects.create(
                    username=player.user.username,
                    wins=0,
                    losses=0,
                    tournaments_won=0
                )
            return redirect('tournament')
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Uno o más jugadores no existen.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

def editprofile(request):
   
    if request.method == 'POST':


        form = EditProfileForm(request.POST, request.FILES)
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
           
            user.set_password(password)
            user.username = nickname
            user.first_name = name
            user.email = email
            user.save()
            stats = UserProfile.objects.get(user=user)
            stats.avatar = avatar
            stats.save()
            # volver a logear al usuario con los nuevos datos   
            
            
            
            login(request, user)
            #log_user = authenticate(request, username=nickname, password=password)
            #stats = UserProfile.objects.get(user=log_user)
            #return render(request, 'signin.html', {'form': form})
            return redirect("/profile", {'log_user': user, 'profile':stats})
        
    else:
        form = RegisterForm(request.GET, request.FILES)
    return render(request, 'editprofile.html', {'form': form, 'loged_user': loged_user})

""" def tournament(request):
    global loged_user, loged_stats
    return render(request, 'tournament.html', {'loged_user':loged_user, 'loged_stats':loged_stats}) """

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

def home_view(request):
    user = User.objects.last()

    victorias = 3 
    derrotas = 5

    context = {
        'user': user,
        'wins': victorias,
        'losses': derrotas,
    }

    return render(request, 'profile.html', context)

# API ENDPOINTS ESPECÍFICOS
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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UsersInTournament
from rest_framework import status
import random

def calculate_win_rate(wins, losses):
    total = wins + losses
    return (wins / total) * 100 if total > 0 else 0

def update_user_tournament_profile(username, wins=0, losses=0, tournaments_won=0):
    """Actualiza un perfil de usuario existente en UsersInTournament."""
    try:
        user = UsersInTournament.objects.get(username=username)
        user.wins += wins
        user.losses += losses
        user.tournaments_won += tournaments_won
        user.save()
        return {
            'username': user.username,
            'wins': user.wins,
            'losses': user.losses,
            'tournaments_won': user.tournaments_won,
        }
    except UsersInTournament.DoesNotExist:
        raise Exception(f"El usuario '{username}' no existe en UsersInTournament.")

@api_view(['GET'])
def get_tournament_players(request):
    def is_power_of_two(n):
        return n > 1 and (n & (n - 1)) == 0

    try:
        total_players = UsersInTournament.objects.count()
        max_power = 1
        while (max_power * 2) <= total_players:
            max_power *= 2
        if max_power < 2:
            return Response({'error': 'No hay suficientes jugadores para un torneo (mínimo 2)'}, status=400)
        players = list(UsersInTournament.objects.order_by('id')[:max_power])
        serialized = [{'username': p.username} for p in players]
        return Response({'players': serialized}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def submit_tournament_match(request):
    winner = request.data.get('winner')
    loser = request.data.get('loser')
    is_final = request.data.get('is_final', False)

    if not winner or not loser:
        return Response({'error': 'Faltan datos: winner y loser son requeridos.'}, status=400)

    try:
        winner_entry, _ = UsersInTournament.objects.get_or_create(username=winner)
        loser_entry, _ = UsersInTournament.objects.get_or_create(username=loser)
        winner_entry.wins += 1
        loser_entry.losses += 1
        if is_final:
            winner_entry.tournaments_won += 1
        winner_entry.save()
        loser_entry.save()
        if is_final:
            sync_users_in_tournament_to_user_profile()

        return Response({'message': 'Partido registrado correctamente'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_players_for_game(request):
    """Devuelve los jugadores disponibles según el tipo de juego."""
    game_type = request.GET.get('game_type', '1vs1')

    try:
        if game_type == '1vs1':
            players = UsersInTournament.objects.order_by('id')[:2]
        elif game_type == 'battleground':
            players = UsersInTournament.objects.order_by('id')[:4]
        elif game_type == 'tron':
            players = UsersInTournament.objects.order_by('id')[:2]
        elif game_type == '1vsIA':
            players = UsersInTournament.objects.order_by('id')[:1]
        else:
            return Response({'error': 'Tipo de juego no soportado'}, status=400)

        serialized_players = [{'username': p.username, 'wins': p.wins, 'losses': p.losses} for p in players]
        return Response({'players': serialized_players}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def update_user_profile(request):
    """Actualiza las estadísticas de un jugador."""
    username = request.data.get('username')
    wins = int(request.data.get('wins', 0))
    losses = int(request.data.get('losses', 0))
    tournaments_won = int(request.data.get('tournaments_won', 0))

    if not username:
        return Response({'error': 'El nombre de usuario es requerido'}, status=400)

    try:
        user = UsersInTournament.objects.get(username=username)
        user.wins += wins
        user.losses += losses
        user.tournaments_won += tournaments_won
        user.save()
        return Response({'message': f'{username} actualizado correctamente.'}, status=200)
    except UsersInTournament.DoesNotExist:
        return Response({'error': f'El usuario {username} no existe.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

def sync_users_in_tournament_to_user_profile():
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            user_profile = UserProfile.objects.get(user__username=user.username)
            user_profile.wins += user.wins
            user_profile.losses += user.losses
            user_profile.tournaments_won += user.tournaments_won
            user_profile.save()
        users_in_tournament.delete()
    except UserProfile.DoesNotExist:
        print("Error: No se encontró el perfil de usuario correspondiente.")
    except Exception as e:
        print(f"Error al sincronizar datos: {str(e)}")

@api_view(['POST'])
def sync_1vs1_stats(request):
    """Sincroniza los datos de UsersInTournament con UserProfile para el modo 1vs1."""
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            user_profile = UserProfile.objects.get(user__username=user.username)
            user_profile.wins += user.wins
            user_profile.losses += user.losses
            user_profile.save()
        users_in_tournament.delete()
        return Response({'message': 'Datos sincronizados correctamente para 1vs1.'}, status=200)
    except Exception as e:
        return Response({'error': f'Error al sincronizar datos: {str(e)}'}, status=500)

@api_view(['POST'])
def sync_1vsIA_stats(request):
    """Sincroniza los datos de UsersInTournament con UserProfile para el modo 1vsIA."""
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            user_profile = UserProfile.objects.get(user__username=user.username)
            user_profile.wins += user.wins
            user_profile.losses += user.losses
            user_profile.save()
        users_in_tournament.delete()
        return Response({'message': 'Datos sincronizados correctamente para 1vsIA.'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def sync_tron_stats(request):
    """Sincroniza los datos de UsersInTournament con UserProfile para el modo Tron."""
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            user_profile = UserProfile.objects.get(user__username=user.username)
            user_profile.wins += user.wins
            user_profile.losses += user.losses
            user_profile.tournaments_won += user.tournaments_won
            user_profile.save()
        users_in_tournament.delete()
        return Response({'message': 'Datos sincronizados correctamente para Tron.'}, status=200)
    except Exception as e:
        return Response({'error': f'Error al sincronizar datos: {str(e)}'}, status=500)

@api_view(['POST'])
def sync_tournament_stats(request):
    """Sincroniza los datos de UsersInTournament con UserProfile para torneo y battleground."""
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            user_profile = UserProfile.objects.get(user__username=user.username)
            user_profile.wins += user.wins
            user_profile.losses += user.losses
            user_profile.tournaments_won += user.tournaments_won
            user_profile.save()
        users_in_tournament.delete()
        return Response({'message': 'Datos sincronizados correctamente para torneo y battleground.'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

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
                mutual.save()
        user_profile.save()

            

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
                mutual.save()
        user_profile.save()


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

