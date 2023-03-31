from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control hop-form-control', 'placeholder':'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control hop-form-control','placeholder':'Password'}))

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control hop-form-control', 'placeholder':'Email'}))
    password1 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control hop-form-control','placeholder':'Password'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control hop-form-control','placeholder':'Password'}))