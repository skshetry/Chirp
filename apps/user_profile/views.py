from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from .models import Photo
# from .forms import PhotoForm


@login_required
def user_profile(request, username=None):
    """The User Profile page view."""
    if User.objects.get(username=username):
        user = User.objects.get(username=username)
        return render(request, "user_profile.html", {
            "user": user,
        })
    else:
        return render("User not found")

# def photo_list(request):
#     photos = Photo.objects.all()
#     if request.method == 'POST':
#         form = PhotoForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('settings:settings')
#     else:
#         form = PhotoForm()
#     return render(request, 'image_list.html', {'rform': form, 'photos': photos})
