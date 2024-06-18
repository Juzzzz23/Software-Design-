from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm 
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm
from django.shortcuts import render

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
            return redirect(reverse('landing', kwargs={'username':username}))
        else:
            messages.error(request, "Incorrect Username or Password")
            return redirect('home')
    else:
        return render(request, 'home.html',)

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

def landing(request, username):
    if request.user.is_authenticated and request.user.username == username:
        return render(request, 'landing.html', {'username':username})
    else:
        return redirect('home')

    
def welcome(request, username):
    if request.user.is_authenticated and request.user.username == username:
        return render(request, 'welcome.html', {'username':username})
    else:
        return redirect('home')
    

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect('landing', username=request.user.username)
    else:
        form = UpdateProfileForm(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': form})

def profile_view(request):
    return render(request, 'profile.html')


    
def planner(request):
    return render(request, 'planner.html')
