from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView


def register(request):


    print(f"Request method: {request.method}")
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        print(f"Form data: {request.POST}")
        print(f"Is form valid?: {form.is_valid()}")
        
        if form.is_valid():
            print("Form is valid. Saving user...") 

            user = form.save()

            login(request, user)
            
            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('users:profile')
        else:
            print(f"Form errors: {form.errors}") 
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def profile(request):
    context = {
        'user': request.user,
    }
    return render(request, 'users/profile.html', context)
