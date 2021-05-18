from django.urls import path

from . import views

urlpatterns = [
    path('create/instructor', views.createInstructor, name='createInstructor'),
    path('create/class', views.createClass, name ='createClass'),
    path('', views.CourseHome, name = 'home'),
    path('create/student', views.createStudent, name = 'createStudent'),
    path('create/signup', views.createSignUp, name = 'createSignUp'),
    path('attendance/<str:class_name>', views.attendance, name = 'attendance'),
]
