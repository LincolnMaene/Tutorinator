from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.contrib.auth import logout
from django import template
from .models import studentQueue
# Create your views here.

def register (request): #function that returns view of register page

    if request.method=='POST': # if user posts to form

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            form.save() #hashes pasword for security and save form

            username=form.cleaned_data.get('username')
            messages.success(request, f'Account Created1!')
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html',{'form': form})

def logout_view(request):

    logout(request)
    return render (request, 'users/logout.html')

def homeView(request): #home page view

    queue=studentQueue.objects.all()
    
    
    queueContext={ #allows us to use django variables in the html template

        'queue':queue
    }
    
    return render (request, 'users/home.html', queueContext)