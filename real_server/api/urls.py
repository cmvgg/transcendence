from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserProfileViewSet)
router.register(r'tournaments', views.TournamentViewSet)



urlpatterns = [
    path('', views.index, name='index'),
    path('playground', views.playground, name='playground'),
    path('about', views.about, name='about'),
    path('select', views.select, name='select'),
    path('profile', views.profile, name='profile'),
    path('signin', views.signIn, name='signin'),
    path('user-profiles/', views.UserProfileList.as_view()),
	#path('tournamet', views.TournamentViewSet.as_view()),
	path('generate_players_names/', views.generate_players_names, name='generate_players_names'),
	path('create-tournament/', views.create_tournament, name='create_tournament'),
    path('tournament-results/', views.tournament_results, name='tournament_results'),
    path('get_players/', views.get_players, name='get_players'),
    path('', include(router.urls)),
]

#claude

from django.urls import path
from . import views

# URLs principales de la aplicación
app_name = 'userprofile'

urlpatterns = [
    # Página de perfil (HTML)
    path('profile/', views.profile_page, name='profile_page'),
    
    # API endpoints para UserProfile
    path('api/userprofile/', views.userprofile_list, name='userprofile_list'),
    path('api/userprofile/<int:profile_id>/', views.userprofile_detail, name='userprofile_detail'),
    path('api/userprofile/create/', views.userprofile_create, name='userprofile_create'),
    path('api/userprofile/<int:profile_id>/update/', views.userprofile_update, name='userprofile_update'),
    path('api/userprofile/<int:profile_id>/delete/', views.userprofile_delete, name='userprofile_delete'),
    
    # Endpoints especiales
    path('api/userprofile/ranking/', views.userprofile_ranking, name='userprofile_ranking'),
    path('api/userprofile/stats/', views.userprofile_stats, name='userprofile_stats'),
]

#claude URLs del proyecto principal (myproject/urls.py):

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('your_app_name.urls')),  # Reemplaza 'your_app_name' con el nombre real de tu app
    path('', views.index, name='index'),
    path('playground', views.playground, name='playground'),
    path('about', views.about, name='about'),
    path('select', views.select, name='select'),
    path('profile', views.profile, name='profile'),
    path('signin', views.signIn, name='signin'),
    path('register', views.register, name='register'),
    path('user-profiles/', views.UserProfileList.as_view()),
	#path('tournamet', views.TournamentViewSet.as_view()),
	path('generate_players_names/', views.generate_players_names, name='generate_players_names'),
	path('create-tournament/', views.create_tournament, name='create_tournament'),
    path('tournament-results/', views.tournament_results, name='tournament_results'),
    path('get_players/', views.get_players, name='get_players'),
    path('', include(router.urls)),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)