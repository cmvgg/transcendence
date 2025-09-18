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

    path('', include('django_prometheus.urls')),

    path('', page_views.index, name='index'),
    path('index', page_views.index, name='index'),
    path('about', page_views.index, name='about'),
    path('tournament', page_views.index, name='tournament'),
    path('tournament.js', page_views.index, name='tournament.js'),

    path('signin', api_views.signIn, name='signin'),
    path('register', api_views.register, name='register'),

    path('update_user_profile/',          api_views.update_user_profile,      name='update_user_profile'),

    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,  document_root=settings.MEDIA_ROOT)
