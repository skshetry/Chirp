from django import forms

from django.contrib.auth.forms import AuthenticationForm

from django.utils.translation import ugettext, ugettext_lazy as _


class CustomUserAuthenticationForm(AuthenticationForm):
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
        widget = forms.PasswordInput(
            attrs = {
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
