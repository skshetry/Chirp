from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from user_profile.forms import UserDetailsForm, UserForm
from django.contrib import messages
from django.contrib.auth import forms
from django.db import transaction


# @login_required
# def settings_view2(request):
#     """The Settings page view."""
#     if request.method == 'POST':
#         user_name_form = forms(request.POST)
#         user_details_form = UserDetailsForm(request.POST)
#         if user_name_form.is_valid() and user_details_form.is_valid():
#             user_name = user_name_form.save(commit=False)
#             user_detail = user_details_form.save(commit=False)
#             user_name.save()
#             user_detail.save()
#             messages.success(request, "Successfully Changed User Details.")
#             return render(request, 'settings.html', {'form': (user_name_form, user_details_form)})
#     else:
#         user_name_form = forms()
#         user_details_form = UserDetailsForm()
#     return render(request, 'settings.html', {'form': (user_name_form, user_details_form)})


@login_required
@transaction.atomic
def settings_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserDetailsForm(request.POST, instance=request.user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('user_profile:user_profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserDetailsForm(instance=request.user)
    return render(request, 'settings.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })