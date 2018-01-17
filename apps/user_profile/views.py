from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def user_profile(request):
    """The User Profile page view."""
    return render(request, 'user_profile.html')
