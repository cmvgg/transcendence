from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, bitches!\n")

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput,ImageField, Textarea