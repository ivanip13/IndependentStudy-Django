from django.contrib import admin
from .models import Instructor, Class, Student, SignUp

# Register your models here.
admin.site.register(Instructor)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(SignUp)
