from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
  email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.', error_messages={'invalid': 'Enter a valid email address.'})
  first_name = forms.CharField(max_length = 20, help_text='Required. Enter your first name.')
  last_name = forms.CharField(max_length = 20, help_text='Required. Enter your last name.')

  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserLoginForm(forms.Form):
  username = forms.CharField(max_length=150, help_text='Required. Enter your username.')
  password = forms.CharField(widget=forms.PasswordInput, help_text='Required. Enter your password.')
