from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from .forms import CustomUserAuthenticationForm as UserAuthenticationForm
from django.utils.safestring import mark_safe
from django.contrib.auth.views import LoginView

# Create your views here.

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserAuthenticationForm
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)
    return redirect('accounts:login')
