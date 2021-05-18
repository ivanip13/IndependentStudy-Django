from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect

from .forms import InstructorForm, ClassForm, StudentForm, SignUpForm
from .models import Class, Student, SignUp, Instructor
from django.db.models import Sum

from django.contrib import messages

# Create your views here.
def CourseHome(request):
    content = {}
    #Retrieve count of each Model
    student_count = Student.objects.all().count()
    instructor_count = Instructor.objects.all().count()
    signup_count = SignUp.objects.all().count()
    class_count = Class.objects.all().count()

    content['student_count'] = student_count
    content['instructor_count'] = instructor_count
    content['signup_count'] = signup_count
    content['class_count'] = class_count

    #Retrieve Remaining INventory
    inventory_sum = Class.objects.aggregate(Sum('inventory')).get('inventory__sum')
    content['inventory_sum'] = inventory_sum

    #Retrieve Recent SignUp
    last_ten = SignUp.objects.all().order_by('-id')[:10]
    content['last_ten'] = last_ten

    #Retrieve Classes with Inventory
    available_am_classes = Class.objects.raw('''SELECT id
                                 FROM course_class
                                 Where inventory > 0 and time = 'AM' ''')
    available_pm_classes = Class.objects.raw('''SELECT id
                                 FROM course_class
                                 Where inventory > 0 and time = 'PM' ''')

    content['available_am_classes'] = available_am_classes
    content['available_pm_classes'] = available_pm_classes

    #Send to render
    return render(request, 'home.html', content)


def createInstructor(request):
    content = {}

    form = InstructorForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Submited Successfully')
            return HttpResponseRedirect('/create/instructor')

    content['form'] = form
    return render(request, 'create_instructor.html', content)

def createClass(request):

    content = {}

    form = ClassForm(request.POST or None, request.FILES or None)
    if request.method == "POST":

        if form.is_valid():
            form.save()
            messages.success(request, 'Submited Successfully')

            return HttpResponseRedirect('/create/class')

    content['form'] = form
    print(content)

    return render(request, 'create_class.html',content)


def createStudent(request):

    content = {}

    form = StudentForm(request.POST or None, request.FILES or None)
    if request.method == "POST":

        if form.is_valid():
            form.save()
            messages.success(request, 'Submited Successfully')

            return HttpResponseRedirect('/create/student')
    content['form'] = form

    available_classes = Class.objects.all()
    # print(available_classes)
    classes =[]
    # for course in available_classes:
    #     classes.append(course.class_name)

    # query = Class.objects.all().values('time')
    query = Class.objects.raw('''SELECT id
                                 FROM course_class''')
    print(query)
    for obj in query:
        classes.append((obj.class_name, obj.time, obj.class_type, obj.class_age))
    content['classes'] = classes
    print(content)

    return render(request, 'create_student.html',content)


def createSignUp(request):

    available_classes = Class.objects.all()
    classes =[]
    query = Class.objects.raw('''SELECT id
                                 FROM course_class
                                 Where inventory > 0''')
    print(query)
    for obj in query:
        classes.append((obj.class_name, obj.time, obj.class_type, obj.class_age, obj.inventory))

    if request.method == "POST":
        form_student = StudentForm(request.POST, prefix = "primary")
        form_signup = SignUpForm(request.POST, prefix = 'signup')
        if form_student.is_valid() and form_signup.is_valid():
            print('both valid')

            #Save Form to Student and SignUp
            student = form_student.save()
            signup = form_signup.save(commit=False)

            print(form_student)
            print(form_signup)
            print(signup.class_AM)
            print(signup.class_PM)


            am_course = Class.objects.filter(class_name = signup.class_AM)
            pm_course = Class.objects.filter(class_name = signup.class_PM)

            # course.inventory -

            #Decrease AM Class and PM Class inventory levels
            for obj in am_course:
                print('Previous AM Inventory', obj.inventory)
                obj.inventory = obj.inventory -1
                print('New AM Inventory' ,obj.inventory)
                obj.save()
            # course.save()
            for obj in pm_course:
                print('Previous PM Inventory', obj.inventory)
                obj.inventory = obj.inventory -1
                print('New PM Inventory' ,obj.inventory)
                obj.save()



            signup.student = student
            signup.save()


            messages.success(request, 'Submited Successfully')

            return HttpResponseRedirect('/create/signup')

        else:
            print('failed')
    else:
        form_student = StudentForm(prefix = "primary")
        form_signup = SignUpForm(prefix = 'signup')

    return render(request, 'signup.html', {
        'student': form_student,
        'signup' : form_signup,
        'classes': classes
    })

def attendance(request, class_name):
    content = {}
    content['class_name'] = class_name
    print(class_name)
    class_type = Class.objects.filter(class_name = class_name)
    print(class_type.values_list())
    print(class_type.values_list()[0][7])
    class_time = class_type.values_list()[0][7]
    print(type(class_time))
    if class_time == 'PM':
        print('afternoon')
        class_attendance = SignUp.objects.filter(class_PM = class_name)
        content['signup'] = class_attendance
    elif class_time == 'AM':
        print('morning')
        class_attendance = SignUp.objects.filter(class_AM = class_name)
        content['signup'] = class_attendance
    print(class_attendance)
    # class_attendance = SignUp.objects.filter()
    # content['signup'] = SignUp.objects.all().select_related("student")
    # print(content['signup'][0].student.age)

    return render(request, 'attendance.html', content)
