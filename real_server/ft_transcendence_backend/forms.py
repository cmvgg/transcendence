from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.db import models


class ExampleForm(models.Form):
    name = forms.CharField(label='Name')
    nickname = forms.CharField(label='Nickname')
    email = forms.EmailField(label='Email')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'get'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Submit'))