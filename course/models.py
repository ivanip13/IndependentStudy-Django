from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime
# Create your models here.

class Instructor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    birthday=models.DateField(auto_now=False, null=True, blank=True)
    medical_certification_choices =(
            ('CPR', 'CPR'),
            ('First Aid', 'First Aid'),
            ('Both', 'Both'),
            ('None', 'None')
        )
    medical_certification = models.CharField(max_length = 50, choices = medical_certification_choices)
    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Class(models.Model):
    year = models.IntegerField(default = datetime.date.today().year)
    class_name = models.CharField(max_length = 50)
    instructor_name = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    class_size = models.IntegerField()
    inventory = models.IntegerField()
    time_choices =(
        ('AM', 'AM'),
        ('PM', 'PM')
    )
    class_type_choices =(
        ('Academic', 'Academic'),
        ('Athletic', 'Athletic'),
        ('Creative', 'Creative')
    )
    class_type = models.CharField(max_length = 8, choices = class_type_choices)
    time = models.CharField(max_length = 2, choices = time_choices)
    class_age_choices =(
        ('YY', 'Younger Youth (7-10)'),
        ('OY', 'Older Youth (11-15)'),
        ('AY', 'All Youth (7-15)')
        )
    class_age =models.CharField(max_length = 2, choices = class_age_choices)
    assistants= models.IntegerField()
    def has_inventory(self):
        return self.inventory > 0

    def __str__(self):
        return self.class_name


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class SignUp(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_AM = models.CharField(max_length=50)
    class_PM = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add = True)
