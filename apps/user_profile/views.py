from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .models import Photo
# from .forms import PhotoForm


@login_required
def user_profile(request):
    """The User Profile page view."""
    return render(request, 'user_profile.html')


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
