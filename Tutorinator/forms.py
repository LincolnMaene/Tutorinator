from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .models import User, Course, Schedule, QueueEntry, Report
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.models import Q

# to automatically add new users to the student group.
student_group = Group.objects.get(name='Student')

class UserRegistrationForm (UserCreationForm):
    
    id = forms.CharField(label = "ID", max_length=20, help_text="Required. 20 characters or fewer. Digits only.")
    first_name = forms.CharField(label = 'First Name', max_length=250)
    last_name = forms.CharField(label = 'Last Name', max_length=250)
    
    class Meta:
        model = User
        fields = ('username', 'id', 'first_name', 'last_name', 'password1', 'password2')
    
    # need to define a special save method so it can create the user correctly, then add extra attributes
    def save(self, commit=True):
        # call base class save method to handle most of the data
        user = super(UserRegistrationForm, self).save(commit=False)
        
        # initialize data not handled by the base class
        user.id = self.cleaned_data['id']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # give them an empty schedule in case they become a tutor one day
        s = Schedule(tutor=user)
        
        # save the user to the database
        if commit:
            user.save()
            s.save()
        
        # make user a student
        student_group.user_set.add(user)
        
        return user

class AddStudentForm(forms.ModelForm):
    id = forms.CharField(label = "ID", max_length=20, help_text="Enter the student's ID.")
    class Meta:
        model=QueueEntry
        fields = ( 'id', 'course' )
        
    def clean(self):
        cd = self.cleaned_data
        
        # if there is no student with the entered id
        if not User.objects.filter(id=cd['id']).exists():
            raise ValidationError('No student with ID ' + cd['id'] + '.')
            
        # if the user exists, but is not a student
        elif not User.objects.filter(id=cd['id']).first().groups.filter(name="Student").exists():
            raise ValidationError("User is not a student.")
            
        return cd
        
    def save(self, commit=True):
        queue_entry = super(AddStudentForm, self).save(commit=False)
        
        # make the user the student, and set the course
        queue_entry.student = User.objects.filter(id=self.cleaned_data['id']).first()
        queue_entry.course = Course.objects.filter(name=self.cleaned_data['course']).first()
        
        if commit:
            queue_entry.save()
        return queue_entry

class AddStudentFormRestricted(forms.ModelForm):
    class Meta:
        model=QueueEntry
        fields = ( 'course', )
        
    def clean(self):
        cd = self.cleaned_data
        
        # unable to pass user in to clean method. not sure if theres a way to verify this here
        # if the user is not a student
        # if not user.groups.filter(name="Student").exists():
        #     raise ValidationError('You are not a student. Only students can be added to the queue.')
        
        # *** looks like django already makes the list of courses for us, so we dont need to verify that it exists
        # # if there is no course with the entered name
        # if not Course.objects.filter(name=cd['course']).exists():
        #     raise ValidationError('No course with name ' + cd['course'] + '.')
        
        return cd
    
    def save(self, user, commit=True):
        queue_entry = super(AddStudentFormRestricted, self).save(commit=False)
        
        # make the user the student, and set the course
        queue_entry.student = user
        queue_entry.course = Course.objects.filter(name=self.cleaned_data['course']).first()
        
        if commit:
            queue_entry.save()
        return queue_entry

class CourseForm(forms.ModelForm):
    class Meta:
        model=Course
        fields = ( 'name', )
    
    def clean(self):
        cd = self.cleaned_data
        if Course.objects.filter(name=cd['name']).exists():
            raise ValidationError('Course with name ' + cd['name'] + ' already exists.')
        
        return cd

class ReportSessionForm(forms.ModelForm):
    report=forms.Textarea
  
    class Meta:
        model=Report
        fields=(
            'queue_entry',
            'text',
        )
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.pid = kwargs.pop('pid', None)
        super(ReportSessionForm, self).__init__(*args, **kwargs)
        
        # only get the list of queue entries where the user is involved
        self.fields['queue_entry'] = forms.ModelChoiceField(queryset=QueueEntry.objects.filter(Q(student=user)|Q(tutor=user)))
    
    def save(self, user, commit=True):
        reportsessionform = super(ReportSessionForm, self).save(commit=False)
        
        # store the user who made the report
        reportsessionform.reporter = user
        
        if commit:
            reportsessionform.save()
        return reportsessionform

class ModifyScheduleForm(forms.Form):
    new_schedule=forms.CharField(widget=forms.Textarea, label='New Schedule')