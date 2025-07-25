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
        form = ExampleForm(request.GET)
    return render(request, 'register.html', {'form': form})


def about(request):
    return render(request, 'about.html')

def select(request):
    return render(request, 'select.html')

def tournament(request):
    return render(request, 'tournament.html')

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
    Endpoint para procesar resultados de un torneo y actualizar estadísticas.
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
        if len(players) < 4:
            return Response({'error': 'Not enough players registered for the tournament'}, status=status.HTTP_400_BAD_REQUEST)

        # Procesar resultados del torneo
        for match in results:
            winner_alias = match.get('winner')
            loser_alias = match.get('loser')

            if winner_alias and loser_alias and winner_alias != "BYE" and loser_alias != "BYE":
                try:
                    winner = UserProfile.objects.get(alias=winner_alias)
                    loser = UserProfile.objects.get(alias=loser_alias)
                except UserProfile.DoesNotExist:
                    print(f"Alias no encontrado: winner={winner_alias}, loser={loser_alias}")
                    continue

                winner.wins += 1
                loser.losses += 1

                winner.save()
                loser.save()

        # Actualizar o copiar datos a api_userTournamentStats
        try:
            cursor.execute( """
                INSERT INTO api_userTournamentStats (user_id, username, wins, losses, tournaments_won)
                SELECT 
                    u.id AS user_id,
                    u.alias AS username,
                    u.wins AS wins,
                    u.losses AS losses,
                    COUNT(CASE WHEN t.id IS NOT NULL AND t.status = 'finished' THEN 1 ELSE NULL END) AS tournaments_won
                FROM api_userprofile u
                LEFT JOIN api_tournament_participants tp ON tp.userprofile_id = u.id
                LEFT JOIN api_tournament t ON t.id = tp.tournament_id
                GROUP BY u.id, u.alias, u.wins, u.losses
            """ )
            with connection.cursor() as cursor:
                for player in players:
                    print(f"Procesando jugador: {player.alias}, ID: {player.id}, Wins: {player.wins}, Losses: {player.losses}")
                    # Verificar si el jugador ya existe en api_userTournamentStats
                    cursor.execute("""
                        SELECT id FROM api_userTournamentStats WHERE user_id = %s
                    """, [player.id])
                    result = cursor.fetchone()

                    if result:
                        # Actualizar estadísticas existentes
                        print(f"Actualizando estadísticas para el jugador: {player.alias}")
                        cursor.execute("""
                            UPDATE api_userTournamentStats
                            SET wins = %s, losses = %s, tournaments_won = CASE WHEN %s = 0 THEN tournaments_won + 1 ELSE tournaments_won END
                            WHERE user_id = %s
                        """, [player.wins, player.losses, player.losses, player.id])
                    else:
                        # Insertar nuevo registro
                        print(f"Insertando nuevo registro para el jugador: {player.alias}")
                        cursor.execute("""
                            INSERT INTO api_userTournamentStats (user_id, username, wins, losses, tournaments_won)
                            VALUES (%s, %s, %s, %s, %s)
                        """, [player.id, player.alias, player.wins, player.losses, 1 if player.losses == 0 else 0])
        except Exception as e:
            print(f"Error al actualizar estadísticas: {e}")

        try:
            tournament.status = 'finished'
            tournament.save()
        except Exception as e:
            return Response({'error': f'Error al guardar el torneo: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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







#claude example

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import UserProfile
import json

# Vista para renderizar la página del perfil
@login_required
def profile_page(request):
    """Vista para mostrar la página de perfil"""
    return render(request, 'profile.html')

# API Views
@require_http_methods(["GET"])
def userprofile_list(request):
    """
    API endpoint para obtener lista de perfiles de usuario
    GET /api/userprofile/
    """
    try:
        # Parámetros de consulta opcionales
        search = request.GET.get('search', '')
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        ordering = request.GET.get('ordering', '-wins')  # Por defecto ordenar por wins descendente
        
        # Filtrar perfiles
        queryset = UserProfile.objects.all()
        
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
def userprofile_detail(request, profile_id):
    """
    API endpoint para obtener un perfil específico
    GET /api/userprofile/{id}/
    """
    try:
        profile = get_object_or_404(UserProfile, id=profile_id)
        
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
        
    except UserProfile.DoesNotExist:
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
def userprofile_create(request):
    """
    API endpoint para crear un nuevo perfil
    POST /api/userprofile/create/
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
        if UserProfile.objects.filter(alias=alias).exists():
            return JsonResponse({
                'success': False,
                'error': 'Este alias ya está en uso'
            }, status=400)
        
        # Crear perfil
        profile = UserProfile.objects.create(
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
def userprofile_update(request, profile_id):
    """
    API endpoint para actualizar un perfil específico
    PUT/PATCH /api/userprofile/{id}/update/
    """
    try:
        profile = get_object_or_404(UserProfile, id=profile_id)
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
            if UserProfile.objects.filter(alias=new_alias).exclude(id=profile_id).exists():
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
        
    except UserProfile.DoesNotExist:
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
def userprofile_delete(request, profile_id):
    """
    API endpoint para eliminar un perfil específico
    DELETE /api/userprofile/{id}/delete/
    """
    try:
        profile = get_object_or_404(UserProfile, id=profile_id)
        alias = profile.alias  # Guardar para el mensaje
        profile.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Perfil "{alias}" eliminado exitosamente'
        })
        
    except UserProfile.DoesNotExist:
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
def userprofile_ranking(request):
    """
    API endpoint para obtener ranking de jugadores
    GET /api/userprofile/ranking/
    """
    try:
        # Parámetros opcionales
        limit = request.GET.get('limit', 10)
        try:
            limit = min(int(limit), 100)  # Máximo 100
        except (ValueError, TypeError):
            limit = 10
        
        # Obtener top jugadores ordenados por wins descendente, luego por alias
        top_profiles = UserProfile.objects.order_by('-wins', 'alias')[:limit]
        
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
            'total_players': UserProfile.objects.count()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error al obtener ranking: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def userprofile_stats(request):
    """
    API endpoint para obtener estadísticas generales
    GET /api/userprofile/stats/
    """
    try:
        from django.db.models import Sum, Avg, Max, Min, Count
        
        stats = UserProfile.objects.aggregate(
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
        best_player = UserProfile.objects.filter(
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