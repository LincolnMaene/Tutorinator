from django.db import models




# Create your models here.

class TimeOffRequest(models.Model): #time off request
    firstName=models.CharField(max_length=250)
    lastName=models.CharField(max_length=250)
    tutorId=models.IntegerField()
    schedule=models.CharField(max_length=3000)
    approved=models.CharField(max_length=250, default='Pending')


class Student(models.Model): #student model
    student_id=models.IntegerField(unique=True)
    firstName=models.CharField(max_length=250)
    lastName=models.CharField(max_length=250)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    tutor=models.BooleanField(default=False) # is the student a tutor?

class Schedules(models.Model): #should allow us to store schedules, ideally
    course=models.CharField(max_length=250) 
    firstName=models.CharField(max_length=250)
    lastName=models.CharField(max_length=250)
    tutorId=models.IntegerField()
    schedule=models.TextField(max_length=3000)


class Administrator(models.Model): #admin model
    admin_id=models.IntegerField(unique=True)
    firstName=models.CharField(max_length=250)
    lastName=models.CharField(max_length=250)
    email=models.EmailField()
    password=models.CharField(max_length=50)

class Reports(models.Model): # model for reports
    day=models.DateField(null=True, auto_now=True)
    student_id=models.IntegerField()
    studentName=models.CharField(max_length=250)
    TutorName=models.CharField(max_length=250)
    course=models.CharField(max_length=250) 
    report=models.TextField(max_length=3000)


class Sessions (models.Model):
    

    day=models.DateField(null=True, auto_now=True) #which day is today
    student_id=models.IntegerField()
    studentName=models.CharField(max_length=250)
    TutorName=models.CharField(max_length=250)
    course=models.CharField(max_length=250) #which course the student needs help with
    sessionBeginTime=models.TimeField(null=True, auto_now=True) #when the tutoring session begun
    sessionEndTime=models.TimeField(null=True) #whn the tutoring session end
    timeTaken=models.DurationField(null=True)# how much time the student has left that day  


class studentQueue (models.Model):
    
    date=models.DateTimeField(auto_now_add=True, blank=True)
    day=models.DateField(null=True, auto_now=True) #which day is today
    student_id=models.IntegerField()
    firstName=models.CharField(max_length=250)
    lastName=models.CharField(max_length=250)
    tutorname=models.CharField(max_length=250, null=True)
    course=models.CharField(max_length=250) #which course the student needs help with
    inQueue=models.BooleanField(default=True) #whetehr or not the student is in the queue or has been removed
    sessionBeginTime=models.TimeField(null=True) #when the tutoring session begun
    sessionEndTime=models.TimeField(null=True) #whn the tutoring session end
    timeLeft=models.DurationField(null=True)# how much time the student has left that day