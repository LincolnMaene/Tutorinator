from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import (UserRegistrationForm, addStudentForm, 
reportForm, ScheduleForm, courseSearchForm, tutorStudentForm,
ModifyScheduleForm, timeOffAcceptForm)
from .forms import timeOffRequestForm
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django import template
from .models import( studentQueue, 
Reports, Schedules, TimeOffRequest,
TimeOffRequest
)
from .models import Reports
from django.views.generic import UpdateView
import datetime
import time
from timeit import default_timer as timer
from django.contrib.auth import views as auth_views

# Create your views here.

queue=None # global variable for the queue of students


class tutorStudentView(UpdateView):
    model=studentQueue
    fields=['student_id','firstName','lastName','course','inQueue']


def timeOffRequestListView(request):

    schedules=TimeOffRequest.objects.all()

    context={

        'schedules':schedules
    }


    return render (request, 'users/timeOffRequestList.html',context)

def homeOrLoginView(request): # redirect the user to either the login (if they havent yet) or the home page (if theyre logged in)
    if (request.user.is_authenticated):
        return (homeView(request))
    else:
        return(auth_views.LoginView.as_view(template_name='users/login.html')(request))

def schedulesView(request):# gives us the schedules listed

    schedules=Schedules.objects.all()

    context={

        'schedules':schedules
    }

    return render (request, 'users/schedules.html',context)

def timeOffRequestView(request):

    form=timeOffRequestForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, f'Request Created!')

    context = {

        'form':form

    }



    return render (request, 'users/timeOffRequest.html', context)

def setSchedulesView(request): #allows us to add schedules

    form=ScheduleForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, f'Schedule Created!')

    context = {

        'form':form

    }



    return render (request, 'users/setSchedules.html', context)

def register (request): #function that returns view of register page

    if request.method=='POST': # if user posts to form

        form = UserRegistrationForm(request.POST)

        if form.is_valid():

            form.save() #hashes pasword for security and save form

            username=form.cleaned_data.get('username') # it is actually possible to get isolated data from a form, fantastic
            messages.success(request, f'Account Created!')
            return redirect('login')

    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html',{'form': form})

def logout_view(request):

    logout(request)
    return render (request, 'users/logout.html')

def courseSearchView(request): #allow us to insert a course to search

    

    if request.method=='POST':

        form=courseSearchForm(request.POST)
        
        if form.is_valid():
            
            course=form.cleaned_data.get('course') # we get the course name from the form            
            messages.success(request, f'Course Entered!')

            return HttpResponseRedirect("/courseLookUp/{course}/".format(course= course))

    else:
        form=courseSearchForm()


    context={

        'form':form
    }

    return render (request,'users/courseSearch.html',context)

def studentView(request, student_id):#allows to tutor students
    
    students=get_object_or_404(studentQueue, student_id=student_id)
    #students=studentQueue.objects.filter(student_id=student_id)

    form=tutorStudentForm(request.POST or None, instance = students)

    if form.is_valid():
        form.save()
        #return HttpResponseRedirect("home")

    context={

        'students': students,
        'form':form
    }

    '''
    if request.method=="POST":
        for student in students:
            student.delete()
        return redirect('home')
    context={
        'students': students
    }
    '''
    return render(request,'users/tutorStudent.html',context)

def modifyScheduleView(request, id):# gives us the schedules listed

    schedules=get_object_or_404(Schedules, id=id)
    
    form=ModifyScheduleForm(request.POST or None, instance = schedules)

    if form.is_valid():
       form.save()

    context={

        'form':form
    }

    return render (request, 'users/modifySchedule.html',context)

def timeOffRequestAcceptView(request, id):

    schedules=get_object_or_404(TimeOffRequest, id=id)

    form=timeOffAcceptForm(request.POST or None, instance = schedules)

    if form.is_valid():
       form.save()

    context={

        'form':form
    }



    return render (request, 'users/modifySchedule.html',context)

def courseLookUpView(request, course):# gives us the schedules listed

    schedules=Schedules.objects.filter(course=course)

    context={

        'schedules':schedules
    }

    return render (request, 'users/courseLookUp.html',context)

def reportView(request):#allows us to add reports about a given session

    form=reportForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, f'Report Created1!')
       

    context = {

        'form':form

    }

    return render (request, 'users/reports.html',context)

def addStudentView(request): #allows us to add students to queue

    today=datetime.datetime.now()# used to ensure only students added to the queue today are compated with
    form=addStudentForm(request.POST or None)

    queue=studentQueue.objects.filter(day=today, inQueue=True)#get all the stds in the queue right now
    

    repeat=False # the idea is to prevent students from signing up twice on the same list
        
   

    if form.is_valid():   

        student_id=form.cleaned_data.get('student_id')   
        
                 
        for student in queue: #try to find out if anyone in the queue has the same id
            
            if student.student_id==17:
                repeat=True

        if repeat==False:
            form.save()
            messages.success(request, f'student added!')

    context = {

        'form': form

    }


    return render (request, 'users/addStudent.html', context)

def reportListView(request): # gives us a list of reports

    reports=Reports.objects.all()

    context={

        'reports': reports

    }

    return render (request, 'users/reportList.html',context)

def homeView(request): #home page view

    today=datetime.datetime.now()# used to ensure only students added to the queue today are displayed
    queue=studentQueue.objects.filter(day=today, inQueue=True)
    
    timeLeft=datetime.timedelta(0,0,0,0,30,0,0) # how much time a student has left, to later be set by admin

    for student in queue:
        student.timeLeft=timeLeft
    
        
    queueContext={ #allows us to use python variables in the html template

        'queue':queue,
    }
    
    return render (request, 'users/home.html', queueContext)

def tutoringRecordView(request): #home page view

    
    queue=studentQueue.objects.all()
    
    queue.order_by('date')
    
        
    queueContext={ #allows us to use python variables in the html template

        'queue':queue,
        
    }
    
    return render (request, 'users/tutoringRecord.html', queueContext)