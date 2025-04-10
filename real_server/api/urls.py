from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet  # Cambia la importación
from django_prometheus.views import metrics
from . import views # Puedes dejar esta línea también, no causará problemas

router = DefaultRouter()
router.register(r'users', views.UserProfileViewSet)

urlpatterns = [
    path('metrics/', metrics, name='prometheus_metrics'),
    path('', views.index, name='index'),
    path('user-profiles/', views.UserProfileList.as_view()),
    path('', include(router.urls)),
]