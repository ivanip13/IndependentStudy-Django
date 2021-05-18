from django import forms
from .models import Instructor, Class, Student, SignUp

class InstructorForm(forms.ModelForm):

    class Meta:
        model = Instructor
        fields = "__all__"

class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = "__all__"

    def clean(self):
        if self.cleaned_data['class_size'] != self.cleaned_data['inventory']:
            print('Inventory and Class Size Do Not Match')
            raise forms.ValidationError("Inventory and Class Size do not match")

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = "__all__"

class SignUpForm(forms.ModelForm):

    class Meta:
        model = SignUp
        exclude = ('student',)
        # fields = "__all__"
