from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Hello, bitches! This is not a bug, you are the bug!\n</h1>")

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

