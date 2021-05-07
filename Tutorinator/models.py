from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# to ensure IDs are numeric
numeric = RegexValidator(r'^[0-9]*$', 'Only numeric characters are allowed.')

# Create your models here.

# model to represent a user
class User(AbstractUser):
    """
    automatically created attributes:
        schedule - schedule used for tutors
        report_set - list of reports this user has made
        student_queueentry_set - list of queue entries where this user is the student
        tutor_queueentry_set - list of queue entries where this user is the tutor
    """
    id = models.CharField(max_length=20, primary_key=True, validators=[numeric])
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
# model representing a course to be taught
class Course(models.Model):
    """
    automatically created attributes:
        schedule_set - list of schedules that contain this course
        queueentry_set - list of queue entries that are for this course
    """
    name=models.CharField(max_length=250, unique=True) # the name of the course
    
    def __str__(self):
        return self.name
    
# model representing the schedule associated with a user
class Schedule(models.Model):
    """
    automatically created attributes:
        none
    """
    tutor=models.OneToOneField(User, on_delete=models.CASCADE) # the tutor who this schedule belongs to
    courses=models.ManyToManyField(Course) # courses that this schedule includes
    schedule=models.CharField(max_length=3000, default="No Schedule")
    change=models.CharField(max_length=3000, default="No Change")
    changed=models.BooleanField(default=False)

# model representing an entry in a queue for a course
class QueueEntry(models.Model):
    """
    automatically created attributes:
        report_set - list of reports that relate to this queue entry
    """
    date=models.DateTimeField(auto_now_add=True, blank=True)
    day=models.DateField(null=True, auto_now=True) #which day is today
    student=models.ForeignKey(User, related_name="student_queueentry_set", null=True, on_delete=models.SET_NULL)
    tutor=models.ForeignKey(User, related_name="tutor_queueentry_set", null=True, on_delete=models.SET_NULL)
    course=models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    inQueue=models.BooleanField(default=True) #whether or not the student is in the queue or has been removed
    sessionBeginTime=models.TimeField(null=True) #when the tutoring session begun
    sessionEndTime=models.TimeField(null=True) #whn the tutoring session end
    timeLeft=models.DurationField(null=True)# how much time the student has left that day
    
    def __str__(self):
        result = str(self.day) or ""
        result += ", "
        result += self.course.name or "Deleted Course"
        result += ", "
        result += str(self.tutor) or "No Tutor"
        result += ", "
        result += str(self.student) or "No Student"
        
        return result
        
        

# model representing a report on a previous queue entry
class Report(models.Model):
    """
    automatically created attributes:
        none
    """
    day=models.DateField(null=True, auto_now=True)
    queue_entry=models.ForeignKey(QueueEntry, null=True, on_delete=models.SET_NULL)
    reporter=models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text=models.TextField(max_length=3000)