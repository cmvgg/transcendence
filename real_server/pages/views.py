from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, bitches!\n")

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput,ImageField, Textarea

"""
class register(forms.Form):
    first_name = forms.CharField(required=True, max_length=255)
    last_name = forms.CharField(required=True, max_length=255)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True, max_length=200)
    address = forms.CharField(max_length=1000, widget=forms.Textarea())

def register(request):

    def __init__(self, *args, **kwargs):
        super(PersonalDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-personal-data-form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('submit_form')
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Name', Div('first_name', css_class='form-group col-4'), Div('last_name', css_class='form-group col-4')),
            Fieldset('Contact data', 'email', 'phone', style="color: brown;"),
            InlineRadios('color'),
            TabHolder(Tab('Address', 'address'), Tab('More Info', 'more_info')))
"""
from django.shortcuts import render
from .forms import ExampleForm
from api.models import UserProfile


def register(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Extraer datos del formulario
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Crear el usuario utilizando el nombre como username
            user = User.objects.create_user(username=name, email=email, password=password)

            # Crear automáticamente el perfil con alias igual a name (o modificar según convenga)
            profile = UserProfile.objects.create(alias=name)

            # Opcional: iniciar sesión automáticamente, enviar un mensaje, redirigir, etc.
           # return redirect('http://localhost:8000/')  # redirige a la página de inicio, por ejemplo

    else:
        form = ExampleForm()
    return render(request, 'register.html', {'form': form})