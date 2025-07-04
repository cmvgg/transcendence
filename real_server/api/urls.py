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
    path('user-profiles/', views.UserProfileList.as_view()),
	#path('tournamet', views.TournamentViewSet.as_view()),
	path('generate_players_names/', views.generate_players_names, name='generate_players_names'),
	path('create-tournament/', views.create_tournament, name='create_tournament'),
    path('tournament-results/', views.tournament_results, name='tournament_results'),
    path('get_players/', views.get_players, name='get_players'),
    path('', include(router.urls)),
]
