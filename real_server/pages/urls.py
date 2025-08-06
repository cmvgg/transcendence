from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Hello, world!
    path('index', views.index, name='index')
    path('playground', views.playground, name='playground')
]


