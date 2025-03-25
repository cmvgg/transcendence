from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet  # Cambia la importación
from . import views # Puedes dejar esta línea también, no causará problemas

router = DefaultRouter()
router.register(r'users', views.UserProfileViewSet)

urlpatterns = [
    path('test/', views.TestView.as_view()),  # Mueve esta línea al principio
    path('user-profiles/', views.UserProfileList.as_view()),
    path('', include(router.urls)),
]