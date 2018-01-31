from PIL import Image
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import User_details


@login_required
def user_profile(request, username=None):
    """The User Profile page view."""
    if User.objects.get(username=username):
        user = User.objects.get(username=username)
        return render(request, "user_profile.html", {
            "user": user,
        })
    else:
        return ("User not found")
    