from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import *
from django.contrib import messages

def home(request):
    return render(request, "home.html")

# AUTH

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                name = user.first_name
                surname = user.last_name
                return render(request, 'home.html', {'name': name, 'surname': surname})
            else:
                form.add_error(None, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            user.save()

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')  # Redirect to the login page or another appropriate page
    else:
        form = RegistrationForm()

    return render(request, 'auth/register.html', {'form': form})

def logout(request):
    return render(request, "home.html")

# _____________