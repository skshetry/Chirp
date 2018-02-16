from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from posts.forms import PostForm, PostMediaFormSet

from .models import User_details

User_model = get_user_model()
@login_required
def user_profile(request, username=None):
    """The User Profile page view."""
    media_form_set = PostMediaFormSet()
    post_form = PostForm()

    if User.objects.filter(username=username).exists():
        user = User.objects.select_related('user_details').prefetch_related('post_set').get(username=username)
        return render(request, "user_profile.html", {
                "profile_user": user,
                "mediaformset": media_form_set,
                "post_form": post_form,
            })
    else:
        return ("User not found")

@login_required
def follow_user(request, username=None):
    toggle_user = get_object_or_404(User_model, username__iexact=username)
    if request.user.is_authenticated():
        is_following = User_details.objects.toggle_follow(request.user, toggle_user.user_details)
    return redirect('user_profile:user_profile', username=username)


@login_required
def profile_photo(request, username=None):
    user = User.objects.get(username=username)
    if user:
        if user.user_details.profile_photo:
            return redirect(user.user_details.profile_photo.url)
        from django.templatetags.static import static as static_tag
        return redirect(static_tag('img/default_profile.jpg'))
