from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import Group

from .forms import AddStudentFormRestricted, UserRegistrationForm, AddStudentForm, CourseForm, ModifyScheduleForm, ReportSessionForm
from .models import User, Course, Schedule, QueueEntry, Report

#useful functions

def returnHome(request):
    messages.warning(request, f'You do not have permission to access this page. You have been redirected to the Home page.')
    return redirect('home')

def isStudent(request):
    return request.user.groups.filter(name="Student").exists()

def isTutor(request):
    return request.user.groups.filter(name="Tutor").exists()

def isAdmin(request):
    return request.user.groups.filter(name="Admin").exists()

# Create your views here.

def homeView(request): #redirects the user to the home page
    return render(request, 'generic/home.html')

def homeOrLoginView(request): # redirect the user to either the login (if they havent logged in yet) or the home page (if theyre logged in)
    if (request.user.is_authenticated):
        return redirect('home')
    else:
        return redirect('login')

def logout_view(request): #redirects user to the logout page
    logout(request)
    return render (request, 'account/logout.html')          

def registerView(request): #provides the form for a user to create an account
    
    form = UserRegistrationForm(request.POST or None)
    
    if form.is_valid():
        form.save() #hashes pasword for security and save form
        messages.success(request, f'Account Created!')
        return redirect('login')
    
    context = { 'form' : form }
    
    return render(request, 'account/register.html', context)

def addStudentView(request): #provides the form to allow students to add themselves to the tutor queue. admins must choose a student by name
    
    if isAdmin(request):
        # admin has unrestricted version of form (can put in student id)
        form=AddStudentForm(request.POST or None)
        
        if form.is_valid():
            coursename=form.cleaned_data['course']
            course=Course.objects.filter(name=coursename)
            
            # make sure the student isnt already in the course's queue
            repeat = False
            if course.exists():
                for entry in course.first().queueentry_set.filter(inQueue=True): #try to find out if the user already exists in the queue for the desired course
                    if entry.student == User.objects.filter(id=form.cleaned_data['id']).first():
                        repeat = True
                
            if repeat:
                messages.warning(request, f'Unable to add student, they are already in the queue for this course.')
            else:
                form.save()
                messages.success(request, f'Student Added!')
        
        context = { 'form': form }
        return render (request, 'queue/addStudent.html', context)
        
    elif isStudent(request):
        # students have a restricted version of the form, they can only enter their desired course
        form=AddStudentFormRestricted(request.POST or None)
    
        if form.is_valid():
            coursename=form.cleaned_data['course']
            course=Course.objects.filter(name=coursename)
             
            # make sure the student isnt already in the course's queue
            repeat = False
            if course.exists():
                for entry in course.first().queueentry_set.filter(inQueue=True): #try to find out if the user already exists in the queue for the desired course
                    if entry.student == request.user:
                        repeat = True
                
            if repeat:
                messages.warning(request, f'Unable to add to course. You are already in the queue for this course.')
            else:
                form.save(request.user)
                messages.success(request, f'You\'ve been Added!')

        context = { 'form': form }
        return render (request, 'queue/addStudent.html', context)
    
    # user is neither a student nor admin (might be a tutor from outside the school system)
    else:
        return returnHome(request)

def addCourseView(request): # allows admins to create a new course that tutors can teach
    if not isAdmin(request):
        return returnHome(request)
    
    form = CourseForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        messages.success(request, f'Course Created!')
        return redirect('courses')
    
    context = { 'form' : form }
    
    return render(request, 'course/addCourse.html', context)

def tutoringRecordView(request): #provides the tutoring records to the admin

    if isAdmin(request):
        queue=QueueEntry.objects.all().order_by('-date')
        queue.order_by('date')
        queueContext={ 
            'queue':queue,
        }
        return render (request, 'queue/tutoringRecord.html', queueContext)   
 
    else:
         return returnHome(request)

def reportView(request): #allows us to add reports about a given session
    if isStudent(request) or isTutor(request):

        form=ReportSessionForm(request.POST or None, user=request.user)

        if form.is_valid():
            form.save(request.user)
            messages.success(request, f'Report Created!')
            return redirect('reports')
            
        context = {
            'form':form
        }
        return render (request, 'report/reports.html',context)
        
    else: # user cant create a report (is most likely an admin)
        return returnHome(request)

def reportListView(request): #provides admins with a list of the reports

    if isAdmin(request):
        reports=Report.objects.all().order_by('-day')
        context={ 'reports': reports }
        return render (request, 'report/reportList.html', context)
        
    else:
        return returnHome(request)

def schedulesView(request):# gives us the schedules listed
    
    # show admins all schedules
    if isAdmin(request):
        schedules=Schedule.objects.filter(tutor__groups__in=Group.objects.filter(name='Tutor'))
        context={ 'schedules' : schedules }
        return render (request, 'schedule/schedules.html',context)
        
    # send non-admins/tutors to the home page
    else:
        return returnHome(request)       

def queueView(request): # shows all queue entries that the user is part of. if the user is an admin, it shows all of them
    
    queue = QueueEntry.objects.filter(inQueue=True).order_by('-date')
    queue_as_student = queue.filter(student=request.user)
    
    if isAdmin(request) or isTutor(request):
        context = { 'queue' : queue }
        return render(request, 'queue/queue.html', context)
    elif isStudent(request):
        context = { 'queue' : queue_as_student }
        return render(request, 'queue/queue.html', context)
    
    return returnHome(request)
    
def queueEntryView(request, id, option = None):
    
    entry = get_object_or_404(QueueEntry, id=id)
    
    if (request.user == entry.student or isTutor(request) or isAdmin(request)):
        
        # handle options from the buttons on the page
        if isAdmin(request):
            if option == 'delete':
                entry.delete()
                return redirect('tutoringRecord')
        
        if isTutor(request):
            if option == 'tutor': # set the tutor of this entry
                if entry.tutor:
                    messages.warning(request, f'Unable to tutor this student, this entry already has a tutor.')
                else:
                    entry.tutor = request.user
                    messages.success(request, f'Successfully became the tutor.')
                    
        if (isStudent(request) and entry.student == request.user) or isAdmin(request):
            if option == 'remove': # remove this entry from the queue
                entry.inQueue=False
        
        
        # save changes to the entry
        entry.save()
        
        has_tutor = entry.tutor is not None
        in_queue = entry.inQueue
        context = { 'entry' : entry, 'in_queue' : in_queue, 'has_tutor': has_tutor }
        return render(request, 'queue/queueEntry.html', context)
    else:
        return returnHome(request)
        
def scheduleView(request, id, option = None):
    
    schedule = get_object_or_404(Schedule, tutor_id=id)
    
    if isTutor(request) or isAdmin(request):
        
        # handle options from the buttons on the page
        if isAdmin(request):
            if option == 'change':
                return redirect('modifySchedule', id)

            if option == 'accept_changes':
                if schedule.changed:
                    schedule.schedule = schedule.change
                    schedule.change = 'No Change'
                    schedule.changed = False
        
        if isTutor(request):
            if option == 'request_change':
                return redirect('modifySchedule', id)
        
        # save changes to the entry
        schedule.save()
        
        context = { 'schedule' : schedule }
        return render(request, 'schedule/schedule.html', context)
        
    else:
        return returnHome(request)
    
def modifyScheduleView(request, id):
    
    schedule = get_object_or_404(Schedule, tutor_id=id)
    form = ModifyScheduleForm(request.POST or None)
    
    if isAdmin(request) or schedule.tutor == request.user: 
        
        if form.is_valid():
            if isAdmin(request):
                schedule.change = "No Change"
                schedule.changed = False
                schedule.schedule = form.cleaned_data['new_schedule']
                messages.success(request, f'Changes Made.')
            else:
                schedule.change = form.cleaned_data['new_schedule']
                schedule.changed = True
                messages.success(request, f'Request Made.')
            schedule.save()
            return redirect('schedule', id)
        
        context = { 'form':form, 'schedule': schedule}
        
        return render(request, 'schedule/modifySchedule.html', context)
        
        
        
    else:
        return returnHome(request)
    
def coursesView(request):
    
    if isAdmin(request):
        courses = Course.objects.all()
        context = { 'courses': list(map(lambda x: (x, x.queueentry_set.filter(inQueue=True).count()), courses)) }
        return render(request, 'course/courses.html', context)
    else:
        return returnHome(request)

def courseView(request, id, option = None):
    
    course = get_object_or_404(Course, id=id)
    
    if isAdmin(request) or isTutor(request):
        
        # to determine if the "Tutor this course" button should be shown. not to be confused with isTutor(), which verifies if the user is a tutor or not
        is_tutor = False
        
        # handle options from the buttons on the page
        if isAdmin(request):
            if option == 'remove':
                messages.success(request, f'Successfully deleted the course: ' + course.name)
                
                for queueentry in course.queueentry_set.all():
                    queueentry.inQueue = False
                    queueentry.save()
                    
                course.delete()
                return coursesView(request)
        elif isTutor(request): # TODO test this for tutors
            if request.user.schedule.courses.filter(id=course.id):
                is_tutor = True
                if option == 'remove_from_schedule':
                    request.user.schedule.courses.remove(course)
                    is_tutor = False
            else:
                if option == 'add_to_schedule':
                    request.user.schedule.courses.add(course)
                    is_tutor = True
            
        # save changes to the course
        course.save()
        
        context = { 'course' : course, 'count' : course.queueentry_set.filter(inQueue=True).count(), 'is_tutor': is_tutor }
        return render(request, 'course/course.html', context)
    else:
        return returnHome(request)