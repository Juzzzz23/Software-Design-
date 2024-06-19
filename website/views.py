from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, PlanForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm
from django import forms
from .models import Plan
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

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

#Registration Form

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
        plans = Plan.objects.filter(user=request.user)
        return render(request, 'landing.html', {'username':username})
    else:
        return redirect('home')

    
def welcome(request, username):
    if request.user.is_authenticated and request.user.username == username:
        return render(request, 'welcome.html', {'username':username})
    else:
        return redirect('home')
    
#Update Profile page

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

#For planner

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['task', 'due_date', 'due_time']

@login_required    
def planner(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect('landing', username=request.user.username)
    else:
        form = PlanForm()
    return render(request, 'planner.html', {'form': form})

def landing(request, username):
    if request.user.is_authenticated and request.user.username == username:
        plans = Plan.objects.filter(user=request.user)
        return render(request, 'landing.html', {'username': username, 'plans': plans})
    else:
        return redirect('home')    
    
def planner(request):
    return render(request, 'planner.html')

@require_POST
@login_required
def complete_plan(request, plan_id):
    try:
        plan = Plan.objects.get(id=plan_id, user=request.user)
        plan.completed = True
        plan.save()
        messages.success(request, "Plan marked as completed!")
    except Plan.DoesNotExist:
        messages.error(request, "Plan does not exist.")
    return redirect('landing', username=request.user.username)

@login_required
def complete_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id, user=request.user)
    plan.completed = True
    plan.save()
    return redirect('landing', username=request.user.username)

def landing(request,username):
    user = request.user
    plans = Plan.objects.filter(user=user)
    return render(request, 'landing.html', {'username': username, 'plans': plans})


def planner_view(request):
    if request.method == 'POST':
        form = PlanForm(request.Post)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect('landing', username=request.user.username)
    else:
        form = PlanForm()
    return render(request, 'planner.html', {'form': form})