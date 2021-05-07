"""Tutorinator2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Tutorinator import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', user_views.homeView), # home page, may redirect to login if user is not authenticated
    path('register/', user_views.registerView, name='register'),
    path('admin/', admin.site.urls, name='admin'), # admin view
    path('home', user_views.homeView, name='home'),
    path('addStudent/', user_views.addStudentView, name='addStudent'),
    path('tutoringRecord/', user_views.tutoringRecordView, name='tutoringRecord'),
    path('reports/', user_views.reportView, name='reports'),
    path('reportsList/', user_views.reportListView, name='reportsList'),
    # path('courseSearch/', user_views.courseSearchView, name='courseSearch'),
    path('schedules/', user_views.schedulesView, name='schedules'),
    path('schedule/<int:id>/', user_views.scheduleView, name='schedule'),
    path('schedule/<int:id>/<option>/', user_views.scheduleView, name='schedule'),
    path('modifySchedule/<int:id>', user_views.modifyScheduleView, name='modifySchedule'),
    # path('modifySchedule/<int:id>/', user_views.modifyScheduleView, name='modifySchedule'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html') , name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html') , name='logout'),
    path('addCourse/', user_views.addCourseView, name='addCourse'),
    path('queue/', user_views.queueView, name = "queue"),
    path('queueEntry/<int:id>/', user_views.queueEntryView, name = 'queueEntry'),
    path('queueEntry/<int:id>/<option>/', user_views.queueEntryView, name = 'queueEntry'),
    path('courses/', user_views.coursesView, name='courses'),
    path('course/<int:id>/', user_views.courseView, name='course'),
    path('course/<int:id>/<option>', user_views.courseView, name='course'),
]
