from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core import urlresolvers

class UserAuthenticationForm(forms.Form):
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

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username).first()
        if not user.is_active:
            raise forms.ValidationError("Your email has not been verified. Please verify")
        else:
            if not user.check_password(password):
                raise forms.ValidationError("Invalid credentials. Wrong username/password.")
        return super(UserAuthenticationForm, self).clean(*args, **kwargs)