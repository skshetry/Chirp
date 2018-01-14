"""Form handling for :accounts:."""
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth.forms import AuthenticationForm

from django.utils.translation import ugettext, ugettext_lazy as _



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First name',
                'required': 'required',
                }
        ))
    last_name = forms.CharField(
        max_length=30, required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': 'required',
                }
        ))
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                    'class': 'form-control',
                    'placeholder': 'Email',
                    'required': 'required',
                    }
        ))

   

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class CustomUserAuthenticationForm(AuthenticationForm):
    """
    CustomUserAuthForm with custom error message.

    Also, adds attributes to the input fields.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': 'required',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'required': 'required',
            }
        )
    )
    AuthenticationForm.error_messages['inactive'] = _(
        "The email has not been verified. Please check your email\
        for verification link."
        )
