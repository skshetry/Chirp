from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core import urlresolvers


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, )
    last_name = forms.CharField(max_length=30, required=False, )
    email = forms.EmailField(max_length=254,)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class UserAuthenticationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

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
