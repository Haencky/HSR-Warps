from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    """
    Login Formular
    """
    username  = forms.CharField(max_length=100, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password  = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class RegistrationForm(UserCreationForm):
    """
    Registration Formular
    """
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class AddPullsForm(forms.Form):
    """
    Add Pull Formular, requires URL
    """

    url = forms.URLField(label='', widget=forms.TextInput(attrs={'placeholder': 'URL'}))

class AddItemManual(forms.Form):
    eng_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Name (eng.)'}))
    