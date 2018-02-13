from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import User_details

User_model = get_user_model()
@login_required
def user_profile(request, username=None):
    """The User Profile page view."""
    if User.objects.get(username=username):
        user = User.objects.get(username=username)
        if user == request.user:
            return render(request, "user_profile.html", {
                "profile_user": user,
            })
        else:
            return render(request, "user_profile.html", {
                "profile_user": user,
            })
    else:
        return ("User not found")

def follow_user(request, username=None):
    toggle_user = get_object_or_404(User_model, username__iexact=username)
    if request.user.is_authenticated():
        is_following = User_details.objects.toggle_follow(request.user, toggle_user.user_details)
    return redirect('user_profile:user_profile', username=username)
