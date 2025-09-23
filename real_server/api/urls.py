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
    path('tron', views.tron, name='tron'),
    path('about', views.about, name='about'),
    path('select', views.select, name='select'),
    #
    path('tmp1vs1', views.tmp1vs1, name='tmp1vs1'),
    path('tmptournament', views.tmptournament, name='tmptournament'),
	path('tmpbattleground', views.tmpbattleground, name='tmpbattleground'),
	path('tmptron', views.tmptron, name='tmptron'),
	path('duplicate_1vsIA/', views.duplicate_1vsIA, name='duplicate_1vsIA'),
	path('duplicate_1vs1/', views.duplicate_1vs1, name='duplicate_1vs1'),
	path('duplicate_tournament/', views.duplicate_tournament, name='duplicate_tournament'),
    path('duplicate_battleground/', views.duplicate_battleground, name='duplicate_battleground'),
    path('duplicate_tron/', views.duplicate_tron, name='duplicate_tron'),
    path('profile', views.profile_view, name='profile'),
    path('signin', views.signIn, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('home', views.home_view, name='home'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('home', views.home_view, name='home'),
    path('user-profiles/', views.UserList.as_view()),
	#
    path('update_user_profile/', views.update_user_profile, name='update_user_profile'),
    path('get_players_for_game/', views.get_players_for_game, name='get_players_for_game'),
    path('get_tournament_players/', views.get_tournament_players, name='get_tournament_players'),
    path('submit_tournament_match/', views.submit_tournament_match, name='submit_tournament_match'),
    path('sync_tournament_stats/', views.sync_tournament_stats, name='sync_tournament_stats'),
    path('sync_1vs1_stats/', views.sync_1vs1_stats, name='sync_1vs1_stats'),
	path('sync_1vsIA_stats/', views.sync_1vsIA_stats, name='sync_1vsIA_stats'),
	path('sync_tron_stats/', views.sync_tron_stats, name='sync_tron_stats'),
    #
    path('', include(router.urls)),
	path('', include('django_prometheus.urls')),
    path('add_friends', views.add_friends, name='add_friends'),
    path('delete_friends', views.delete_friends, name='delete_friends'),
]

