from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

from .models import UserProfile
from .serializers import UserProfileSerializer

class UserProfileList(APIView):
    """
    Lista todos los perfiles de usuario o crea uno nuevo.
    """
    def get(self, request, format=None):
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y editar perfiles de usuario.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


""" para crear un formulario de crispy forms
    https://www.makeuseof.com/django-crispy-forms-style/
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput,ImageField, Textarea

class RegisterUserForm(UserCreationForm):
        email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class PersonalDataForm(forms.Form):
    first_name = forms.CharField(required=True, max_length=255)
    last_name = forms.CharField(required=True, max_length=255)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True, max_length=200)
    address = forms.CharField(max_length=1000, widget=forms.Textarea())

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
            TabHolder(Tab('Address', 'address'), Tab('More Info', 'more_info'))
        )