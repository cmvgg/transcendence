from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserProfileViewSet)
router.register(r'tournaments', views.TournamentViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('user-profiles/', views.UserProfileList.as_view()),
    path('tournament-results/', views.tournament_results, name='tournament_results'),
    path('get_players/', views.get_players, name='get_players'),
    path('', include(router.urls)),
	path('', include('django_prometheus.urls')),
]
