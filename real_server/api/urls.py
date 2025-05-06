from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet 
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', views.UserProfileViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('/playground', views.index, name='playground'),
    path('/about', views.index, name='about'),
    path('/select', views.index, name='select'),
    path('user-profiles/', views.UserProfileList.as_view()),
    path('', include(router.urls)),
	path('', include('django_prometheus.urls')),
]