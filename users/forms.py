from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from .models import studentQueue
from .models import Student
from .models import Sessions
from .models import Reports, Schedules, TimeOffRequest


class UserRegistrationForm (UserCreationForm):
    email=forms.EmailField()
    student_id=forms.IntegerField()

    class Meta:
        model=User
        fields=['username','email','student_id']


class StudentRegistrationForm (forms.ModelForm):
    class Meta:
        model=Student
        fields=[ 'student_id','firstName','lastName','email','password']


class tutorStudentForm(forms.ModelForm): #allows us to tuttor students to queue
    
    class Meta:
        model=studentQueue
        fields = [
            'student_id',
            'firstName',
            'lastName',
            'course',
            'inQueue'
        
        ]

class addStudentForm(forms.ModelForm): #allows us to add students to queue
    
    class Meta:
        model=studentQueue
        fields = [
            'student_id',
            'firstName',
            'lastName',
            'course',
        
        ]

class addSessionForm(forms.ModelForm): #allows us to add students to queue

   
    class Meta:
        model=Sessions
        fields = [
            'student_id',
            'studentName',
            'TutorName',
            'course'
        ]

class reportForm(forms.ModelForm):
    report=forms.Textarea
   
    class Meta:
        model=Reports
        fields=[

            'student_id',
            'studentName',
            'TutorName',
            'course',
            'report'
        ]

class ScheduleForm(forms.ModelForm):

    schedule=forms.Textarea
    class Meta:
        model=Schedules
        fields=[
        
        'course',
        'firstName',
        'lastName',
        'tutorId',
        'schedule'
        
        ]

class timeOffRequestForm(forms.ModelForm):
    schedule=forms.CharField(widget=forms.Textarea, label='Insert Time and Reason for Request')
    class Meta:
        model=TimeOffRequest
        fields=[
        
       
        'firstName',
        'lastName',
        'tutorId',
        'schedule'
        
        ]


class courseSearchForm(forms.Form):

    course=forms.CharField(label='Your Course', max_length=300)

    