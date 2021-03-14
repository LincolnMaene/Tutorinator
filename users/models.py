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
   


