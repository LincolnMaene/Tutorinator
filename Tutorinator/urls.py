"""Tutorinator URL Configuration

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
from django.shortcuts import redirect
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', user_views.homeView, name='home'),
    path('admin/', admin.site.urls, name = 'admin'),
    path('register/', user_views.register, name='register'),
    path('addStudent/', user_views.addStudentView, name='addStudent'),
    path('reports/', user_views.reportView, name='reports'),
    path('reportsList/', user_views.reportListView, name='reportsList'),
    path('courseSearch/', user_views.courseSearchView, name='courseSearch'),
    path('timeOffRequest/', user_views.timeOffRequestView, name='timeOffRequest'),
    path('timeOffRequestList/', user_views.timeOffRequestListView, name='timeOffRequestList'),
    path('courseLookUp/<str:course>/', user_views.courseLookUpView, name='courseLookUp'),
    path('setSchedules/', user_views.setSchedulesView, name='setSchedules'),
    path('schedules/', user_views.schedulesView, name='schedules'),
    path('student/<int:student_id>/', user_views.studentView, name='student'),
    path('modifySchedule/<int:id>/', user_views.modifyScheduleView, name='modifySchedule'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html') , name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html') , name='logout'),
    
]
