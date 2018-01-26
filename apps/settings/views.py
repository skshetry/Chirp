from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_profile.forms import UserDetailsForm, UserForm
from django.contrib import messages
from django.contrib.auth import forms
from django.db import transaction


@login_required
@transaction.atomic
def settings_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserDetailsForm(request.POST, instance=request.user.user_details)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save(commit=False)
            profile_form.user = request.user
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('user_profile:user_profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserDetailsForm(instance=request.user.user_details)
    return render(request, 'settings.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })