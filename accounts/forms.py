from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    """
    Registration form used on the sign-up page.

    Extends Django's UserCreationForm (which already provides
    username + password1/password2 with validation) and adds the
    extra fields we need: email, first name and last name.
    """

    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        error_messages={'invalid': 'Enter a valid email address.'}
    )
    first_name = forms.CharField(max_length=20, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=20, help_text='Required. Enter your last name.')

    class Meta:
        model = User
        # Fields rendered on the registration form, in order.
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class UserLoginForm(forms.Form):
    """Simple username/password form used on the login page."""

    username = forms.CharField(max_length=150, help_text='Required. Enter your username.')
    password = forms.CharField(widget=forms.PasswordInput, help_text='Required. Enter your password.')
