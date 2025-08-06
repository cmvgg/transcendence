# ft_transcendence_backend/urls.py
"""
URL configuration for ft_transcendence_backend project.
"""

from django.contrib import admin
from django.urls import path, include
# Import views from pages (only index) and api views for auth and profile
from pages import views as page_views
from api import views as api_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API REST
    path('', include('api.urls')),

    # Métricas Prometheus
    path('', include('django_prometheus.urls')),

    # Vistas estáticas / Reactivas (pages app)
    path('index', page_views.index, name='index'),
    path('about', page_views.index, name='about'),
    path('tournament', page_views.index, name='tournament'),
    path('tournament.js', page_views.index, name='tournament.js'),

    # Autenticación propia y perfil (api app)
    path('signin', api_views.signIn, name='signin'),
    path('register', api_views.register, name='register'),
    #path('profile', api_views.profile, name='profile'),

    # Endpoints de API específicas
    path('update_user_profile/',          api_views.update_user_profile,      name='update_user_profile'),
    path('generate_players_names_1vs1/',  api_views.generate_players_names_1vs1, name='generate_players_names_1vs1'),
    path('generate_players_names/',       api_views.generate_players_names,     name='generate_players_names'),
    path('create-tournament/',            api_views.create_tournament,          name='create_tournament'),
    path('tournament-results/',           api_views.tournament_results,         name='tournament_results'),
    path('get_players/',                  api_views.get_players,                name='get_players'),

    # URLs de autenticación de Django (login/logout/password)
    path('accounts/', include('django.contrib.auth.urls')),
]

# Servir media y estáticos en desarrollo
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
