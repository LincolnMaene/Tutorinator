from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserRegistrationForm, addStudentForm, reportForm
from django.contrib.auth import logout
from django import template
from .models import studentQueue
from .models import Reports
import datetime
import time
from timeit import default_timer as timer

# Create your views here.

queue=None # global variable for the queue of students


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


def studentView(request, student_id):#allows to dynamically look up students in the queue based on their id
    
    student=get_object_or_404(studentQueue, student_id=student_id)

    if request.method=="POST":
        student.delete()
        return redirect('/')
    context={
        'student': student
    }

    return render(request,'users/student.html',context)

def reportView(request):#allows us to add reports about a given session

    form=reportForm(request.POST or None)

    if form.is_valid():
        form.save()

    context = {

        'form':form

    }

    return render (request, 'users/reports.html',context)



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
    
    timeLeft=datetime.timedelta(0,0,0,0,30,0,0) # how much time a student has left, to later be set by admin

    for student in queue:
        student.timeLeft=timeLeft
    
        
    queueContext={ #allows us to use python variables in the html template

        'queue':queue,
        'today':today
    }
    
    return render (request, 'users/home.html', queueContext)