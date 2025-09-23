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
import json
from django.contrib.auth import authenticate, login
from .serializers import (
    UserSerializer,
    TournamentSerializer,
)
from .forms import signInForm, RegisterForm, EditProfileForm

loged_user = None
loged_stats = None

from django.shortcuts import redirect
def index(request):
    global loged_user, loged_stats
    return render(request, 'index.html', {'loged_user':loged_user, 'loged_stats':loged_stats})

def playground(request):
    users_in_tournament = UsersInTournament.objects.all()
    if users_in_tournament.count() < 2:
        users_in_tournament.delete()
        return render(request, 'error.html', {
            'message': "Not enougth players to play 1vs1.",
            'redirect_url': 'select',
            'redirect_text': 'Return'
        })
    top = UserProfile.objects.order_by('wins').last()
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'playground.html', {'profile': profile, 'high_score': top})

def playground2(request):
    users_in_tournament = UsersInTournament.objects.all()
    if not request.user.is_authenticated:
        return render(request, 'error.html', {
            'message': "Your are not logged in to play 1vsIA.",
            'redirect_url': 'select',
            'redirect_text': 'Return'
        })
    if users_in_tournament.count() < 1:
        users_in_tournament.delete()
        return render(request, 'error.html', {
            'message': "Your cannot play 1vsIA again.",
            'redirect_url': 'select',
            'redirect_text': 'Return'
        })
    top = UserProfile.objects.order_by('wins').last()
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'playground_copy.html', {'profile': profile, 'high_score': top})

def battleground(request):
    users_in_tournament = UsersInTournament.objects.all()
    if users_in_tournament.count() < 4:
        users_in_tournament.delete()
        return render(request, 'error.html', {
            'message': "Not enougth players to play  battleground (min 4).",
            'redirect_url': 'select',
            'redirect_text': 'Return'
        })
    top = UserProfile.objects.order_by('wins').last()
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'battleground.html', {'profile': profile, 'high_score': top})

def tron(request):
    users_in_tournament = UsersInTournament.objects.all()
    if users_in_tournament.count() < 2:
        users_in_tournament.delete()
        return render(request, 'error.html', {
            'message': "Not enougth players to play tron.",
            'redirect_url': 'select',
            'redirect_text': 'Return'
        })
    top = UserProfile.objects.order_by('wins').last()
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'playground_tron.html', {'profile': profile, 'high_score': top})

def tournament(request):
    users_in_tournament = UsersInTournament.objects.all()
    if users_in_tournament.count() < 4:
        users_in_tournament.delete()
        return render(request, 'error.html', {
            'message': "Not enougth players to play a tournament (min 4).",
            'redirect_url': 'select',
            'redirect_text': 'Return'
        })
    top = UserProfile.objects.order_by('wins').last()
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'tournament.html', {'profile': profile, 'high_score': top})

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
    user = User
    if user != None:
        logout(request)
        return redirect("/")

import django.contrib.messages as messages
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            nickname = form.cleaned_data.get('nickname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            avatar = form.cleaned_data.get('avatar')
            if User.objects.filter(username=nickname).exists():
                    messages.error(request, 'This username already exists.')
            else:
                    user = User.objects.create_user(first_name=name, email=email, password=password, username=nickname)
                    login(request, user)
                    profile = UserProfile.objects.get(user = user)
                    profile.avatar = avatar
                    profile.save()
                    
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
    users = list(UserProfile.objects.filter(is_online=True))
    current_user = request.user
    users.sort(key=lambda u: u.user.id != current_user.id)
    if not request.user.is_authenticated:
        return render(request, 'error.html', {
            'message': "You are not loggedin.",
            'redirect_url': 'select',
            'redirect_text': 'Log in'
        })
    return render(request, '1vs1_waitlist.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'users': users, 'current_user': current_user})

def tmpbattleground(request):
    global loged_user, loged_stats
    users = list(UserProfile.objects.filter(is_online=True))
    current_user = request.user
    users.sort(key=lambda u: u.user.id != current_user.id)
    if not request.user.is_authenticated:
        return render(request, 'error.html', {
            'message': "You are not loggedin.",
            'redirect_url': 'select',
            'redirect_text': 'Log in'
        })
    return render(request, 'battleground_waitlist.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'users': users, 'current_user': current_user})

def tmptron(request):
    global loged_user, loged_stats
    users = list(UserProfile.objects.filter(is_online=True))
    current_user = request.user
    users.sort(key=lambda u: u.user.id != current_user.id)
    if not request.user.is_authenticated:
        return render(request, 'error.html', {
            'message': "You are not loggedin.",
            'redirect_url': 'select',
            'redirect_text': 'Log in'
        })
    return render(request, 'tron_waitlist.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'users': users, 'current_user': current_user})

def tmptournament(request):
    global loged_user, loged_stats
    users = list(UserProfile.objects.filter(is_online=True))
    current_user = request.user
    users.sort(key=lambda u: u.user.id != current_user.id)
    if not request.user.is_authenticated:
        return render(request, 'error.html', {
            'message': "You are not loggedin.",
            'redirect_url': 'select',
            'redirect_text': 'Log in'
        })
    return render(request, 'tournament_waitlist.html', {'loged_user': loged_user, 'loged_stats': loged_stats, 'users': users, 'current_user': current_user})

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
                wins=0,
                losses=0,
                tournaments_won=0
            )
            return JsonResponse({'redirect_url': '/playground2'}, status=200)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Logged user has not a profile asociated.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Not allowed method..'}, status=405)

@csrf_exempt
def duplicate_1vs1(request):
    if request.method == 'POST':
        try:
            selected_player_ids = request.POST.getlist('player_ids[]')
            if not selected_player_ids or len(selected_player_ids) != 2:
                return JsonResponse({'error': 'You need exactly 2 players for 1vs1.'}, status=400)
            UsersInTournament.objects.all().delete()
            for player_id in selected_player_ids:
                player = UserProfile.objects.get(user_id=player_id)
                UsersInTournament.objects.create(
                    username=player.user.username,
                    avatar=player.avatar,
                    wins=0,
                    losses=0,
                    tournaments_won=0
                )
            return redirect('playground')
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'One or more players dont exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Not allowed method.'}, status=405)

@csrf_exempt
def duplicate_battleground(request):
    if request.method == 'POST':
        try:
            selected_player_ids = request.POST.getlist('player_ids[]')
            if not selected_player_ids or len(selected_player_ids) < 4:
                return JsonResponse({'error': 'You need exactly 4 players to jugar.'}, status=400)
            UsersInTournament.objects.all().delete()
            for player_id in selected_player_ids:
                player = UserProfile.objects.get(user_id=player_id)
                UsersInTournament.objects.create(
                    username=player.user.username,
                    avatar=player.avatar,
                    wins=0,
                    losses=0,
                    tournaments_won=0 
                )
            return redirect('battleground')
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'One or more players dont exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Not allowed method.'}, status=405)

@csrf_exempt
def duplicate_tron(request):
    if request.method == 'POST':
        try:
            selected_player_ids = request.POST.getlist('player_ids[]')
            if not selected_player_ids or len(selected_player_ids) < 2:
                return JsonResponse({'error': 'You need exactly 2 players to play.'}, status=400)
            UsersInTournament.objects.all().delete()
            for player_id in selected_player_ids:
                player = UserProfile.objects.get(user_id=player_id)
                UsersInTournament.objects.create(
                    username=player.user.username,
                    avatar=player.avatar,
                    wins=0,
                    losses=0,
                    tournaments_won=0 
                )
            return redirect('tron')
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'One or more players dont exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Not allowed method.'}, status=405)

from math import log2
@csrf_exempt
def duplicate_tournament(request):
    if request.method == 'POST':
        try:
            selected_player_ids = request.POST.getlist('player_ids[]')
            if not selected_player_ids or len(selected_player_ids) < 4:
                return JsonResponse({'error': 'You need at least 4 players to play a tournament.'}, status=400)
            if log2(len(selected_player_ids)) % 1 != 0:
                return JsonResponse({'error': 'The number of players must be a power of 2 (4, 8, 16, 32, etc.).'}, status=400)
            UsersInTournament.objects.all().delete()
            for player_id in selected_player_ids:
                player = UserProfile.objects.get(user_id=player_id)
                UsersInTournament.objects.create(
                    username=player.user.username,
                    avatar=player.avatar,
                    wins=0,
                    losses=0,
                    tournaments_won=0
                )
            return redirect('tournament')
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'One or more players dont exist.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Not allowed method.'}, status=405)

def editprofile(request):
   
    if request.method == 'POST':


        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            avatar = form.cleaned_data.get('avatar')
            user = request.user
           
            user.set_password(password)
            user.first_name = name
            user.email = email
            user.save()
            stats = UserProfile.objects.get(user=user)
            stats.avatar = avatar
            stats.save()

            login(request, user)
            return redirect("/profile", {'log_user': user, 'profile':stats})
        
    else:
        form = EditProfileForm(request.GET, request.FILES)
    return render(request, 'editprofile.html', {'form': form, 'loged_user': loged_user})

""" def tournament(request):
    global loged_user, loged_stats
    return render(request, 'tournament.html', {'loged_user':loged_user, 'loged_stats':loged_stats}) """

# API VIEWS
class UserList(APIView):
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
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TournamentViewSet(viewsets.ModelViewSet):
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

# API ENDPOINTS
def profile_view(request):
    logedUser = request.user
    username = logedUser.username
    profile = UserProfile.objects.get(user = logedUser)
    

    if request.user.is_authenticated:
        logedUser = request.user
        profile = UserProfile.objects.get(user = logedUser)
        friends_usernames = User.objects.filter(id__in=profile.friends).values_list('username', flat=True)
        friends_online = UserProfile.objects.filter(id__in=profile.friends).values_list('is_online', 'user')
        cucus = User.objects.filter(id__in=profile.friends)
        matches = MatchHistory.objects.filter(winner=username) | MatchHistory.objects.filter(loser=username)
    return render(request, 'profile.html', {
        'profile': profile,
        'friends_names': friends_usernames,
        'friends_online': friends_online, 
        'cucus': cucus,
        'matches': matches
    })

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UsersInTournament
from rest_framework import status
import random

def calculate_win_rate(wins, losses):
    total = wins + losses
    return (wins / total) * 100 if total > 0 else 0

def update_user_tournament_profile(username, wins=0, losses=0, tournaments_won=0):
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
        raise Exception(f"User '{username}' isnt in UsersInTournament.")

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
            return Response({'error': 'There are not enough players for a tournament (min 2)'}, status=400)
        players = list(UsersInTournament.objects.order_by('id')[:max_power])
        serialized = [{
                'username': p.username,
                'avatar': f"/media/{p.avatar.name}" if p.avatar else None
            } 
            for p in players
        ]
        return Response({'players': serialized}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def submit_tournament_match(request):
    winner = request.data.get('winner')
    loser = request.data.get('loser')
    is_final = request.data.get('is_final', False)

    if not winner or not loser:
        return Response({'error': 'You need more data: winner and loser are required.'}, status=400)

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

        return Response({'message': 'Match save correctly'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def get_players_for_game(request):
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
            return Response({'error': 'Game tipe not supported'}, status=400)

        serialized_players = [{
            'username': p.username,
            'wins': p.wins,
            'losses': p.losses,
            'avatar': p.avatar.name if p.avatar else None
        } for p in players]
        return Response({'players': serialized_players}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def update_user_profile(request):
    username = request.data.get('username')
    wins = int(request.data.get('wins', 0))
    losses = int(request.data.get('losses', 0))
    tournaments_won = int(request.data.get('tournaments_won', 0))
    score = int(request.data.get('score', 0))

    if not username:
        return Response({'error': 'The users name is required'}, status=400)

    try:
        user = UsersInTournament.objects.get(username=username)
        user.wins += wins
        user.losses += losses
        user.tournaments_won += tournaments_won
        user.score += score
        user.save()
        return Response({'message': f'{username} update correctly.'}, status=200)
    except UsersInTournament.DoesNotExist:
        return Response({'error': f'User {username} doesnt exist.'}, status=404)
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
        print("Error: User profile couldnt be found")
    except Exception as e:
        print(f"Error syncing data: {str(e)}")

from .models import MatchHistory

@api_view(['POST'])
def sync_1vs1_stats(request):
    try:
        users_in_tournament = list(UsersInTournament.objects.all())

        if len(users_in_tournament) != 2:
            return Response({'error': 'Expected exactly 2 users in tournament'}, status=400)

        for user in users_in_tournament:
            user_profile = UserProfile.objects.get(user__username=user.username)
            user_profile.wins += user.wins
            user_profile.losses += user.losses
            user_profile.save()

        user1, user2 = users_in_tournament

        if user1.wins > user2.wins:
            winner, loser = user1, user2
        else:
            winner, loser = user2, user1

        match = MatchHistory.objects.create(
            winner=winner.username,
            loser=loser.username,
            w_points=winner.score,
            l_points=loser.score,
            type_game='1vs1',
            date=timezone.now()
        )
        users_in_tournament.delete()

        return Response({'message': 'Data correctly synced for 1vs1.'}, status=200)

    except Exception as e:
        import traceback
        return Response({'error': str(e), 'trace': traceback.format_exc()}, status=500)

@api_view(['POST'])
def sync_1vsIA_stats(request):
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            user_profile = UserProfile.objects.get(user__username=user.username)
            user_profile.wins += user.wins
            user_profile.losses += user.losses
            user_profile.save()
        users_in_tournament.delete()
        return Response({'message': 'Data correctly synced for 1vsIA.'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def sync_tron_stats(request):
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            user_profile = UserProfile.objects.get(user__username=user.username)
            user_profile.wins += user.wins
            user_profile.losses += user.losses
            user_profile.tournaments_won += user.tournaments_won
            user_profile.save()

        user1, user2 = users_in_tournament

        if user1.wins > user2.wins:
            winner, loser = user1, user2
        else:
            winner, loser = user2, user1

        match = MatchHistory.objects.create(
            winner=winner.username,
            loser=loser.username,
            w_points=1,
            l_points=0,
            type_game='tron',
            date=timezone.now()
        )
        users_in_tournament.delete()
        return Response({'message': 'Data correctly synced for Tron.'}, status=200)
    except Exception as e:
        return Response({'error': f'Error syncing data: {str(e)}'}, status=500)

@api_view(['POST'])
def sync_tournament_stats(request):
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            user_profile = UserProfile.objects.get(user__username=user.username)
            user_profile.wins += user.wins
            user_profile.losses += user.losses
            user_profile.tournaments_won += user.tournaments_won
            user_profile.save()
        users_in_tournament.delete()
        return Response({'message': 'Data correctly synced for tournament and battleground.'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#user friends
from django.contrib.auth import get_user_model

User = get_user_model()

def add_friends(request):
    if request.method == 'POST':
        users_selected_ids = request.POST.getlist('users_selected')
        users_selected = User.objects.filter(id__in=users_selected_ids)

        user = request.user
        user_profile = UserProfile.objects.get(user = user)
        
        for tmp_user in users_selected:
            if tmp_user != user:
                user_profile.friends.append(tmp_user.id)
                mutual = UserProfile.objects.get(user=tmp_user)
                mutual.friends.append(user.id)
                mutual.save()
        user_profile.save()
        context = {'users_selected': users_selected}
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
        users_selected = User.objects.all()
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
        users_selected = User.objects.all().exclude(id__in=user_profile.friends)
        context = {'users_selected': users_selected}
        return render(request, 'add_friends.html', context)


def delete_friends(request):
    if request.method == 'POST':
        users_selected_ids = request.POST.getlist('user_list')
        users_selected = User.objects.filter(id__in=users_selected_ids)

        user = request.user
        user_profile = UserProfile.objects.get(user = user)
        for tmp_user in users_selected:
            if tmp_user != user:
                user_profile.friends.remove(tmp_user.id)
                mutual = UserProfile.objects.get(user=tmp_user)
                mutual.friends.remove(user.id)
                mutual.save()
        user_profile.save()


        context = {'user_list': users_selected}
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
        user = request.user
        user_profile = UserProfile.objects.get(user = user)
        user_list = User.objects.filter(id__in=user_profile.friends)
        context = {'user_list': user_list}
        return render(request, 'delete_friends.html', context)

