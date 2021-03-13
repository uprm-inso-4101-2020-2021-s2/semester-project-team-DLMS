from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Students, Enrolled_Courses
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import *
from django.core.exceptions import *
from .forms import Enrolled_CoursesForm


# Create your views here.
def register_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username=email, email=email, password=password1, first_name=first_name,
                                                last_name=last_name)
                user.save()
                new_student = Students.objects.create(student_user=user, student_program='None', student_campus='None')
                new_student.save()

                user = authenticate(request, username=email, password=password1)

                if user is not None:
                    login(request, user)
                    return redirect('/home')

            except IntegrityError:
                # TODO: CHANGE
                print("DUMB")

    return render(request, 'UPR_Grader/register.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect("/")

    return render(request, 'UPR_Grader/login.html', )


def home_page(request):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)

    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('../')

    name = request.user.first_name + ' ' + request.user.last_name
    context = {'name': name,
               'campus': request.user.students.student_campus,
               'program': request.user.students.student_program,
               'overall_gpa': request.user.students.student_gpa,
               'major_gpa': request.user.students.student_major_gpa
               }

    return render(request, 'UPR_Grader/home.html', context)


def settings_page(request):
    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)

    student_data = Students.objects.all()
    current_student = Students.objects.filter(student_user=request.user.id)

    if request.method == 'POST':
        campus = request.POST.get('campus', None)
        program = request.POST.get('program', None)
        logout_request = request.POST.get('logout', None)
        delete_request = request.POST.get('delete_request', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('../')

        if request.user.is_authenticated and program is not None:
            Students.objects.filter(student_user=request.user.id).update(student_program=program)

        if request.user.is_authenticated and campus is not None:
            Students.objects.filter(student_user=request.user.id).update(student_campus=campus)

        if request.user.is_authenticated and delete_request is not None:
            Students.objects.filter(student_user=request.user.id).delete()
            request.user.delete()
            logout(request)
            return redirect('../')

    return render(request, 'UPR_Grader/settings.html', {'data': student_data, 'current_student': current_student})


def courses_list(request):
    # List of courses
    list = Enrolled_Courses.objects.all()

    if request.method == 'POST':
        logout_request = request.POST.get('logout', None)

        if request.user.is_authenticated and logout_request is not None:
            logout(request)
            return redirect('../')

    return render(request, 'UPR_Grader/list.html', {'list': list})


def courses_page(request):
    # Creating an empty form
    form = Enrolled_CoursesForm()

    if request.method == "POST":
        # adding receive data to form
        form = Enrolled_CoursesForm(request.POST)
        # checking if form is valid
        if form.is_valid():
            # creating an instance to manage form
            # Delete,edit or add a new course

            instance = form.save(commit=False)

            instance.save()

            return redirect('/list')

    return render(request, 'UPR_Grader/courses.html', {'form': form})


def edit_courses(request, id):
    # course instance
    instance = Enrolled_Courses.objects.get(id=id)

    # creating form with instance data
    form = Enrolled_CoursesForm(instance=instance)

    if request.method == "POST":
        # Updating form
        form = Enrolled_CoursesForm(request.POST, instance=instance)
        # checking if form is valid
        if form.is_valid():
            # Saving form without confirming
            # In that way we have an instance to manage it
            instance = form.save(commit=False)

            instance.save()

            return redirect('/list')

    return render(request, 'UPR_Grader/edit.html', {'form': form})


def delete_courses(request, id):

    instance = Enrolled_Courses.objects.get(id=id)
    instance.delete()

    return redirect('/list')

