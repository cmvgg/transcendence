from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.utils import timezone

def index(request):
    return render(request, 'index.html')

from .models import UserProfile, Tournament
from .serializers import UserProfileSerializer, TournamentSerializer, TournamentResultSerializer

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

class TournamentViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y editar torneos.
    """
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

@api_view(['POST'])
def tournament_results(request):
    """
    Endpoint para procesar resultados de un torneo, tomando los participantes desde la base de datos.
    """
    serializer = TournamentResultSerializer(data=request.data)
    if serializer.is_valid():
        tournament_id = serializer.validated_data['tournament_id']

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)

        players = list(tournament.participants.all())

        if len(players) < 2:
            return Response({'error': 'Not enough players registered for the tournament'}, status=status.HTTP_400_BAD_REQUEST)

    
        results = serializer.validated_data['results']
        for result in results:
            winner_alias = result.get('winner')
            loser_alias = result.get('loser')

            if winner_alias and loser_alias and winner_alias != "BYE" and loser_alias != "BYE":
                try:
                    winner = UserProfile.objects.get(alias=winner_alias)
                    loser = UserProfile.objects.get(alias=loser_alias)
                except UserProfile.DoesNotExist:
                    continue 

                winner.wins += 1
                loser.losses += 1

                winner.save()
                loser.save()

        return Response({
            'status': 'success',
            'tournament_id': tournament.id,
            'message': f'Resultados procesados para torneo "{tournament.name}"'
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput, Textarea

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
