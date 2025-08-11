from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tournaments', views.TournamentViewSet)



urlpatterns = [
    path('', views.index, name='index'),
    path('playground', views.playground, name='playground'),
	path('playground2', views.playground2, name='playground2'),
	path('battleground', views.battleground, name='battleground'),
	path('tournament', views.tournament, name='tournament'),
    path('about', views.about, name='about'),
    path('select', views.select, name='select'),
    #path('profile', views.profile, name='profile'),
    path('signin', views.signIn, name='signin'),
    path('register', views.register, name='register'),
    path('home', views.home_view, name='home'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('home', views.home_view, name='home'),
    path('user-profiles/', views.UserList.as_view()),
    # API endpoints
	#
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
	path('get_players_for_game/', views.get_players_for_game, name='get_players_for_game'),
    path('generate_players_names_1vs1/', views.generate_players_names_1vs1, name='generate_players_names_1vs1'),
    path('get_tournament_players/', views.get_tournament_players, name='get_tournament_players'),
    path('submit_tournament_match/', views.submit_tournament_match, name='submit_tournament_match'),
    path('sync_tournament_stats/', views.sync_tournament_stats, name='sync_tournament_stats'),
    path('sync_1vs1_stats/', views.sync_1vs1_stats, name='sync_1vs1_stats'),
	path('sync_1vsIA_stats/', views.sync_1vsIA_stats, name='sync_1vsIA_stats'),
    #
    path('', include(router.urls)),
	path('', include('django_prometheus.urls')),
]

