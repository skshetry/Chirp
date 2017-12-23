from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from .forms import UserAuthenticationForm
from django.utils.safestring import mark_safe

# Create your views here.

def login_view(request):
    if request.method == 'GET':
        authentication_form = UserAuthenticationForm()
    elif request.method == 'POST':
        authentication_form = UserAuthenticationForm(request.POST)
        if authentication_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('upload_pic')
    return render(request, 'accounts/login.html', {'form':authentication_form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login')
