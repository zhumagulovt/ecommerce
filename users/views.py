from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView

from .forms import CustomUserCreationForm, CustomLoginForm


def login_view(request):
    user = request.user
    # if user.is_authenticated:
    #     return redirect('/')

    if request.method == "POST":
        form = CustomLoginForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        
        if user:
            login(request, user)
            messages.success(request, "Logged in")
            return redirect('/')
        else:
            messages.error(request, "please Correct below errors")

    else:
        form = CustomLoginForm()
    
    return render(request, "users/login.html", {"form": form})

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})