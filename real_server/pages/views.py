from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, bitches!\n")

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput,ImageField, Textarea

from django.shortcuts import render
from .forms import ExampleForm

def register(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Do something with the form data
            pass
    else:
        form = ExampleForm()
    return render(request, 'register.html', {'form': form})

def playground(request):
    
    return render(request, 'playground.html')

def about(request):
    
    return render(request, 'about.html')

def select(request):
    
    return render(request, 'select.html')