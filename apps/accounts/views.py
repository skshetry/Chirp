"""Views for :accounts: handling."""
from django.shortcuts import render, redirect

from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import CustomUserAuthenticationForm as UserAuthenticationForm
from .forms import SignUpForm
from .tokens import account_activation_token


def signup(request):
    if request.user.is_authenticated():
        return redirect('feeds:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Welcome to Chirp.'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'accounts/email_sent.html', { 'email':user.email})
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
    




def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('feeds:home')
        

    else:
        return HttpResponse('Activation link is invalid!')


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
