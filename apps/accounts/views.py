"""Views for :accounts: handling."""
from django.shortcuts import redirect

from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

from .forms import CustomUserAuthenticationForm as UserAuthenticationForm


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
