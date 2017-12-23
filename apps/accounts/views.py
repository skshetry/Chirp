from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import UserAuthenticationForm
from django.utils.safestring import mark_safe
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

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
