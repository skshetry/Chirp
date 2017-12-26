"""Views for :accounts: handling."""
from django.shortcuts import render, redirect

from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout

from .forms import CustomUserAuthenticationForm as UserAuthenticationForm
from .forms import SignUpForm


def signup(request):
    """Create user."""
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
    """
    This handles login view.

    This logs in user using `UserAuthenticationForm`
    and redirects if user is already logged in.
    If there's `next` parameter, it redirects to it after :POST:.
    If login fails, the same view is shown with helpful error message.
    """

    template_name = 'accounts/login.html'
    authentication_form = UserAuthenticationForm
    redirect_authenticated_user = True


def logout_view(request):
    """Logout the user."""
    logout(request)
    return redirect('accounts:login')
