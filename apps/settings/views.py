from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_profile.forms import UserDetailsForm, UserForm
from django.contrib import messages
from django.contrib.auth import forms
from django.db import transaction
from django.core.urlresolvers import reverse
from user_profile.forms import ProfilePhotoForm, CoverPhotoForm

def profile_photo_view(request):
    profile_photo_form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user.user_details)
    if profile_photo_form.is_valid():
        profile_photo_form.save()
        messages.success(request, ('Your profile Photo was successfully updated!'))
        return redirect(reverse('user_profile:user_profile', kwargs={'username': request.user.username}))
    else:
        messages.error(request, ('Cant update profile photo'))



def cover_photo_view(request):
    cover_photo_form = CoverPhotoForm(request.POST, request.FILES, instance=request.user.user_details)
    if cover_photo_form.is_valid():
        cover_photo_form.save()
        messages.success(request, ('Your cover Photo was successfully updated!'))
        return redirect(reverse('user_profile:user_profile', kwargs={'username': request.user.username}))
    else:
        messages.error(request, ('Cant update cover photo'))



@login_required
@transaction.atomic
def settings_view(request):
    if request.method == 'POST':
        if 'profile_submit_button' in request.POST:
            return profile_photo_view(request)

        if 'cover_submit_button' in request.POST:
            return cover_photo_view(request)

        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserDetailsForm(request.POST, instance=request.user.user_details)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save(commit=False)
            profile_form.user = request.user
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect(reverse('user_profile:user_profile', kwargs={'username': request.user.username}))
        else:
            messages.error(request, ('Please correct the error below.'))
    elif request.method == 'GET':
        user_form = UserForm(instance=request.user)
        profile_form = UserDetailsForm(instance=request.user.user_details)
        profile_photo_form = ProfilePhotoForm(instance=request.user.user_details)
        cover_photo_form = CoverPhotoForm(instance=request.user.user_details)

        return render(request, 'settings.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile_photo_form': profile_photo_form,
            'cover_photo_form': cover_photo_form,


            })




