from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

from .forms import CustomUserAuthenticationForm as UserAuthenticationForm
from .forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = UserAuthenticationForm
    redirect_authenticated_user = True

def logout_view(request):
    logout(request)
    return redirect('accounts:login')
