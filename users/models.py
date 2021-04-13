from django.db import models

# Create your models here.
class Student(models.Model): #student model
    student_id=models.IntegerField(unique=True)
    firstName=models.CharField(max_length=250)
    lastName=models.CharField(max_length=250)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    tutor=models.BooleanField(default=False) # is the student a tutor?


class Administrator(models.Model): #admin model
    admin_id=models.IntegerField(unique=True)
    firstName=models.CharField(max_length=250)
    lastName=models.CharField(max_length=250)
    email=models.EmailField()
    password=models.CharField(max_length=50)
   


class studentQueue (models.Model):
    
    date=models.DateTimeField(auto_now_add=True, blank=True)
    day=models.DateField(null=True, auto_now=True)
    student_id=models.IntegerField(unique=True)
    firstName=models.CharField(max_length=250)
    lastName=models.CharField(max_length=250)
    course=models.CharField(max_length=250) #which course the student needs help with