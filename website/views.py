from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm 

def home(request):
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('landing')
        else:
            messages.success(request, "Incorrect Username or Password")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})

def landing(request):
    if request.user.is_authenticated:
        return render(request, 'landing.html', {})
    else:
        return redirect('home')

    
def welcome(request):
    if request.user.is_authenticated:
        return render(request, 'welcome.html', {})
    else:
        return redirect('home')
