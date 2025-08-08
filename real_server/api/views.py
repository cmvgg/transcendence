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
import json, random
from .models import UserProfile, Tournament, TournamentStats

# Importar modelos y serializers
from .models import User, Tournament, Match
from .serializers import (
    UserSerializer,
    TournamentSerializer,
    TournamentResultSerializer
)
from .forms import signInForm, ExampleForm

def index(request):
    return render(request, 'index.html')

def playground(request):
    return render(request, 'playground.html')

def playground2(request):
    return render(request, 'playground_copy.html')


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
                'total_losses': total_losses,
                'total_games': total_games,
            },
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
    return render(request, 'about.html')

def select(request):
    return render(request, 'select.html')

def signIn(request):
    form_s = signInForm()
    return render(request, 'signin.html', {'form': form_s})

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

def tournament(request):
    return render(request, 'tournament.html')

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
        players = UserProfile.objects.all()
    
    serializer = UserSerializer(players, many=True)
    return Response(serializer.data)









from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TournamentStats, UsersInTournament
from rest_framework import status
import random

def calculate_win_rate(wins, losses):
    total = wins + losses
    return (wins / total) * 100 if total > 0 else 0

def generate_random_player_names_1vs1():
    """Genera nombres aleatorios únicos para 1vs1."""
    base_names = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon', 'Zeta','Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']
    return random.sample(base_names, 4)

def create_user_profile(username, wins=0, losses=0, tournaments_won=0):
    """Crea un nuevo perfil de usuario en UsersInTournament."""
    user = UsersInTournament.objects.create(
        username=username,
        wins=wins,
        losses=losses,
        tournaments_won=tournaments_won
    )
    TournamentStats.objects.create(
        username=username,
        wins=wins,
        losses=losses,
        tournaments_won=tournaments_won
    )
    return {
        'username': user.username,
        'wins': user.wins,
        'losses': user.losses,
        'tournaments_won': user.tournaments_won,
    }

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

        # Buscar la mayor potencia de 2 posible con los jugadores disponibles
        max_power = 1
        while max_power * 2 <= total_players:
            max_power *= 2

        if max_power < 2:
            return Response({'error': 'No hay suficientes jugadores para un torneo (mínimo 2)'}, status=400)

        # Obtener los primeros max_power jugadores
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
        # Actualizar datos en UsersInTournament
        winner_entry, _ = UsersInTournament.objects.get_or_create(username=winner)
        loser_entry, _ = UsersInTournament.objects.get_or_create(username=loser)

        winner_entry.wins += 1
        loser_entry.losses += 1

        if is_final:
            winner_entry.tournaments_won += 1

        winner_entry.save()
        loser_entry.save()

        # Si el torneo ha finalizado, sincronizar con TournamentStats
        if is_final:
            sync_users_in_tournament_to_stats()

        return Response({'message': 'Partido registrado correctamente'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def generate_players_names_1vs1(request):
    """Genera jugadores aleatorios e inicializa sus stats."""
    try:
        player_names = generate_random_player_names_1vs1()
        created_players = []
        for name in player_names:
            data = create_user_profile(name, wins=0, losses=0)
            created_players.append(data)

        return Response({
            'status': 'success',
            'message': 'Jugadores generados e inicializados.',
            'players': created_players
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_players_for_game(request):
    """Devuelve los primeros jugadores disponibles según el tipo de juego."""
    game_type = request.GET.get('game_type', '1vs1')

    try:
        if game_type == '1vs1':
            players = UsersInTournament.objects.order_by('id')[:2]
        elif game_type == 'battleground':
            players = UsersInTournament.objects.order_by('id')[:4]
        elif game_type == '1vsIA':
            players = UsersInTournament.objects.order_by('id')[:1]
        else:
            return Response({'error': 'Tipo de juego no soportado'}, status=status.HTTP_400_BAD_REQUEST)

        serialized_players = [{
            'username': p.username,
            'wins': p.wins,
            'losses': p.losses
        } for p in players]

        return Response({'players': serialized_players}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update_user_profile(request):
    """Actualiza las estadísticas de un jugador."""
    username = request.data.get('username')
    wins = int(request.data.get('wins', 0))
    losses = int(request.data.get('losses', 0))

    if not username:
        return Response({'error': 'username es requerido'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = update_user_tournament_profile(username, wins, losses)
        return Response({
            'status': 'success',
            'message': f'{username} actualizado correctamente.',
            'data': data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def sync_users_in_tournament_to_stats():
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            stats_entry, _ = TournamentStats.objects.get_or_create(username=user.username)
            stats_entry.wins += user.wins
            stats_entry.losses += user.losses
            stats_entry.tournaments_won += user.tournaments_won
            stats_entry.save()
        UsersInTournament.objects.all().delete()
    except Exception as e:
        print(f"Error al sincronizar datos: {str(e)}")
        raise Exception(f"Error al sincronizar datos: {str(e)}")

@api_view(['POST'])
def sync_1vs1_stats(request):
    """Sincroniza los datos de UsersInTournament con TournamentStats para el modo 1vs1."""
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            stats_entry, _ = TournamentStats.objects.get_or_create(username=user.username)
            stats_entry.wins += user.wins
            stats_entry.losses += user.losses
            stats_entry.tournaments_won += user.tournaments_won
            stats_entry.save()
        users_in_tournament.delete()
        return Response({'message': 'Datos sincronizados correctamente para 1vs1.'}, status=200)
    except Exception as e:
        return Response({'error': f'Error al sincronizar datos: {str(e)}'}, status=500)


@api_view(['POST'])
def sync_1vsIA_stats(request):
    """Sincroniza los datos de UsersInTournament con TournamentStats para el modo 1vsIA."""
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            stats_entry, _ = TournamentStats.objects.get_or_create(username=user.username)
            stats_entry.wins += user.wins
            stats_entry.losses += user.losses
            stats_entry.save()
        UsersInTournament.objects.all().delete()
        return Response({'message': 'Datos sincronizados correctamente para 1vsIA.'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def sync_tournament_stats(request):
    """Sincroniza los datos de UsersInTournament con TournamentStats para torneo y battleground."""
    try:
        users_in_tournament = UsersInTournament.objects.all()
        for user in users_in_tournament:
            stats_entry, _ = TournamentStats.objects.get_or_create(username=user.username)
            stats_entry.wins += user.wins
            stats_entry.losses += user.losses
            stats_entry.tournaments_won += user.tournaments_won
            stats_entry.save()
        UsersInTournament.objects.all().delete()
        return Response({'message': 'Datos sincronizados correctamente para torneo y battleground.'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)













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
#            profile = User.objects.create(alias=user.username)
#            return redirect('index')
#    else:
#        form = RegisterUserForm()
#    return render(request, 'register.html', {'form': form})

#claude example

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import User
import json

# Vista para renderizar la página del perfil
@login_required
def profile_page(request):
    """Vista para mostrar la página de perfil"""
    return render(request, 'profile.html')

# API Views
@require_http_methods(["GET"])
def user_list(request):
    """
    API endpoint para obtener lista de perfiles de usuario
    GET /api/user/
    """
    try:
        # Parámetros de consulta opcionales
        search = request.GET.get('search', '')
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        ordering = request.GET.get('ordering', '-wins')  # Por defecto ordenar por wins descendente
        
        # Filtrar perfiles
        queryset = User.objects.all()
        
        # Búsqueda por alias
        if search:
            queryset = queryset.filter(
                Q(alias__icontains=search)
            )
        
        # Ordenamiento
        valid_orderings = ['wins', '-wins', 'losses', '-losses', 'alias', '-alias']
        if ordering in valid_orderings:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('-wins', 'alias')  # Ordenamiento por defecto del modelo
        
        # Paginación
        try:
            page_size = min(int(page_size), 100)  # Máximo 100 por página
            paginator = Paginator(queryset, page_size)
            profiles_page = paginator.get_page(page)
        except (ValueError, TypeError):
            profiles_page = Paginator(queryset, 10).get_page(1)
        
        # Serializar datos
        profiles_data = []
        for profile in profiles_page:
            profiles_data.append({
                'id': profile.id,
                'alias': profile.alias,
                'wins': profile.wins,
                'losses': profile.losses,
                'win_rate': profile.win_rate(),
                'total_games': profile.wins + profile.losses,
            })
        
        return JsonResponse({
            'success': True,
            'data': profiles_data,
            'pagination': {
                'current_page': profiles_page.number,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': profiles_page.has_next(),
                'has_previous': profiles_page.has_previous(),
                'next_page': profiles_page.next_page_number() if profiles_page.has_next() else None,
                'previous_page': profiles_page.previous_page_number() if profiles_page.has_previous() else None,
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def user_detail(request, profile_id):
    """
    API endpoint para obtener un perfil específico
    GET /api/user/{id}/
    """
    try:
        profile = get_object_or_404(User, id=profile_id)
        
        data = {
            'id': profile.id,
            'alias': profile.alias,
            'wins': profile.wins,
            'losses': profile.losses,
            'win_rate': profile.win_rate(),
            'total_games': profile.wins + profile.losses,
            'win_rate_percentage': round(profile.win_rate() * 100, 1),
        }
        
        return JsonResponse({
            'success': True,
            'data': data
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Perfil de usuario no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def user_create(request):
    """
    API endpoint para crear un nuevo perfil
    POST /api/user/create/
    """
    try:
        data = json.loads(request.body)
        
        # Validar datos requeridos
        alias = data.get('alias', '').strip()
        if not alias:
            return JsonResponse({
                'success': False,
                'error': 'El alias es obligatorio'
            }, status=400)
        
        # Verificar que el alias sea único
        if User.objects.filter(alias=alias).exists():
            return JsonResponse({
                'success': False,
                'error': 'Este alias ya está en uso'
            }, status=400)
        
        # Crear perfil
        profile = User.objects.create(
            alias=alias,
            wins=data.get('wins', 0),
            losses=data.get('losses', 0)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Perfil creado exitosamente',
            'data': {
                'id': profile.id,
                'alias': profile.alias,
                'wins': profile.wins,
                'losses': profile.losses,
                'win_rate': profile.win_rate(),
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Formato JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al crear perfil: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def user_update(request, profile_id):
    """
    API endpoint para actualizar un perfil específico
    PUT/PATCH /api/user/{id}/update/
    """
    try:
        profile = get_object_or_404(User, id=profile_id)
        data = json.loads(request.body)
        
        # Actualizar campos permitidos
        if 'alias' in data:
            new_alias = data['alias'].strip()
            if not new_alias:
                return JsonResponse({
                    'success': False,
                    'error': 'El alias no puede estar vacío'
                }, status=400)
            
            # Verificar que el nuevo alias sea único (excepto el perfil actual)
            if User.objects.filter(alias=new_alias).exclude(id=profile_id).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Este alias ya está en uso'
                }, status=400)
            
            profile.alias = new_alias
        
        if 'wins' in data:
            wins = data['wins']
            if isinstance(wins, int) and wins >= 0:
                profile.wins = wins
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Las victorias deben ser un número entero no negativo'
                }, status=400)
        
        if 'losses' in data:
            losses = data['losses']
            if isinstance(losses, int) and losses >= 0:
                profile.losses = losses
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Las derrotas deben ser un número entero no negativo'
                }, status=400)
        
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Perfil actualizado exitosamente',
            'data': {
                'id': profile.id,
                'alias': profile.alias,
                'wins': profile.wins,
                'losses': profile.losses,
                'win_rate': profile.win_rate(),
                'total_games': profile.wins + profile.losses,
            }
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Perfil no encontrado'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Formato JSON inválido'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al actualizar perfil: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def user_delete(request, profile_id):
    """
    API endpoint para eliminar un perfil específico
    DELETE /api/user/{id}/delete/
    """
    try:
        profile = get_object_or_404(User, id=profile_id)
        alias = profile.alias  # Guardar para el mensaje
        profile.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Perfil "{alias}" eliminado exitosamente'
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Perfil no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al eliminar perfil: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def user_ranking(request):
    """
    API endpoint para obtener ranking de jugadores
    GET /api/user/ranking/
    """
    try:
        # Parámetros opcionales
        limit = request.GET.get('limit', 10)
        try:
            limit = min(int(limit), 100)  # Máximo 100
        except (ValueError, TypeError):
            limit = 10
        
        # Obtener top jugadores ordenados por wins descendente, luego por alias
        top_profiles = User.objects.order_by('-wins', 'alias')[:limit]
        
        ranking_data = []
        for index, profile in enumerate(top_profiles, 1):
            ranking_data.append({
                'position': index,
                'id': profile.id,
                'alias': profile.alias,
                'wins': profile.wins,
                'losses': profile.losses,
                'win_rate': profile.win_rate(),
                'win_rate_percentage': round(profile.win_rate() * 100, 1),
                'total_games': profile.wins + profile.losses,
            })
        
        return JsonResponse({
            'success': True,
            'data': ranking_data,
            'total_players': User.objects.count()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener ranking: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def user_stats(request):
    """
    API endpoint para obtener estadísticas generales
    GET /api/user/stats/
    """
    try:
        from django.db.models import Sum, Avg, Max, Min, Count
        
        stats = User.objects.aggregate(
            total_players=Count('id'),
            total_wins=Sum('wins'),
            total_losses=Sum('losses'),
            avg_wins=Avg('wins'),
            avg_losses=Avg('losses'),
            max_wins=Max('wins'),
            min_wins=Min('wins'),
            max_losses=Max('losses'),
            min_losses=Min('losses'),
        )
        
        # Calcular estadísticas adicionales
        total_games = (stats['total_wins'] or 0) + (stats['total_losses'] or 0)
        global_win_rate = (stats['total_wins'] or 0) / total_games if total_games > 0 else 0
        
        # Jugador con mejor win rate
        best_player = User.objects.filter(
            wins__gt=0, losses__gte=0
        ).extra(
            select={'win_rate': 'wins::float / NULLIF(wins + losses, 0)'}
        ).order_by('-win_rate', '-wins').first()
        
        return JsonResponse({
            'success': True,
            'data': {
                'general_stats': {
                    'total_players': stats['total_players'],
                    'total_games': total_games,
                    'total_wins': stats['total_wins'] or 0,
                    'total_losses': stats['total_losses'] or 0,
                    'global_win_rate': round(global_win_rate, 3),
                    'global_win_rate_percentage': round(global_win_rate * 100, 1),
                },
                'averages': {
                    'avg_wins_per_player': round(stats['avg_wins'] or 0, 1),
                    'avg_losses_per_player': round(stats['avg_losses'] or 0, 1),
                },
                'extremes': {
                    'max_wins': stats['max_wins'] or 0,
                    'min_wins': stats['min_wins'] or 0,
                    'max_losses': stats['max_losses'] or 0,
                    'min_losses': stats['min_losses'] or 0,
                },
                'best_player': {
                    'id': best_player.id if best_player else None,
                    'alias': best_player.alias if best_player else None,
                    'win_rate': best_player.win_rate() if best_player else 0,
                    'wins': best_player.wins if best_player else 0,
                    'losses': best_player.losses if best_player else 0,
                } if best_player else None
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener estadísticas: {str(e)}'
        }, status=500)