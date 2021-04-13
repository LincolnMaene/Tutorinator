from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserRegistrationForm, addStudentForm
from django.contrib.auth import logout
from django import template
from .models import studentQueue
import datetime
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

def addStudentView(request): #allows us to add students to queue

    form=addStudentForm(request.POST or None)

    if form.is_valid():

        form.save()

    context = {

        'form': form

    }


    return render (request, 'users/addStudent.html', context)



def homeView(request): #home page view

    today=datetime.datetime.now()# used to ensure only students added to the queue today are displayed
    queue=studentQueue.objects.filter(day=today)
    
    
        
    queueContext={ #allows us to use django variables in the html template

        'queue':queue,
        'today':today
    }
    
    return render (request, 'users/home.html', queueContext)