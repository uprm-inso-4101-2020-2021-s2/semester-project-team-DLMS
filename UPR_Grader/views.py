from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Students, Enrolled_Courses, Program_Courses, StudentCourses, Courses
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import *
from django.core.exceptions import *
from .forms import Enrolled_CoursesForm, Curriculum_Form, Edit_Form


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
                print("Integrity Error")

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

    # Calculating Overall GPA
    student_courses = StudentCourses.objects.filter(student=request.user.id).select_related('course')
    honor_points = 0
    total_credits = 0
    for i in student_courses:
        course_grade = i.course_grade
        course_credits = i.course.course_credits
        total_credits = total_credits + course_credits
        if course_grade == 'A':
            honor_points = honor_points + 4 * course_credits
        elif course_grade == 'B':
            honor_points = honor_points + 3 * course_credits
        elif course_grade == 'C':
            honor_points = honor_points + 2 * course_credits
        elif course_grade == 'D':
            honor_points = honor_points + 1 * course_credits
        elif course_grade == 'F':
            honor_points = honor_points + 0 * course_credits

    if honor_points != 0 and total_credits != 0:
        overall_gpa = honor_points / total_credits
        Students.objects.filter(student_user=request.user.id).update(student_gpa=round(overall_gpa, 2))
    else:
        Students.objects.filter(student_user=request.user.id).update(student_gpa=0.0)

    # Calculating Major GPA
    major_honor_points = 0
    major_total_credits = 0
    if Students.objects.filter(student_user=request.user.id).first().student_program == "ICOM":
        for i in student_courses:
            if i.course.course_code[:4] == "ICOM" or i.course.course_code[:4] == "INEL":
                course_grade = i.course_grade
                course_credits = i.course.course_credits
                major_total_credits = major_total_credits + course_credits
                if course_grade == 'A':
                    major_honor_points = major_honor_points + 4 * course_credits
                elif course_grade == 'B':
                    major_honor_points = major_honor_points + 3 * course_credits
                elif course_grade == 'C':
                    major_honor_points = major_honor_points + 2 * course_credits
                elif course_grade == 'D':
                    major_honor_points = major_honor_points + 1 * course_credits
                elif course_grade == 'F':
                    major_honor_points = major_honor_points + 0 * course_credits

    if major_honor_points != 0 and major_total_credits != 0:
        major_gpa = major_honor_points / major_total_credits
        Students.objects.filter(student_user=request.user.id).update(student_major_gpa=round(major_gpa, 2))
    else:
        Students.objects.filter(student_user=request.user.id).update(student_major_gpa=0.0)

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
    list = Enrolled_Courses.objects.filter(student_id=request.user.id)

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
        instance = Enrolled_Courses.objects.create(course_credits=request.POST.getlist('course_credits')[0], course_title=request.POST.getlist('course_title')[0],
                                                   student_id=request.user.id, course_code=request.POST.getlist('course_code')[0])

        instance.save()

        return redirect('/list')

    return render(request, 'UPR_Grader/courses.html', {'form': form})


def edit_courses(request, id):
    # course instance
    instance = Enrolled_Courses.objects.get(id=id)

    # creating form with instance data
    form = Edit_Form(instance=instance)

    if request.method == "POST":
        # Updating form
        form = Edit_Form(request.POST, instance=instance)
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


def curriculum_page(request):
    form = Curriculum_Form()
    program = request.user.students.student_program
    program_courses = Program_Courses.objects.select_related('program', 'course').order_by('semester').filter(program=program)
    program_courses_list = []
    courses_taken = StudentCourses.objects.filter(student=request.user.id).select_related('course')
    submit_button = request.POST.get('submitButton', None)
    home_button = request.POST.get('homeButton', None)

    if home_button is not None:
        return redirect('../home')

    for course in program_courses:
        program_courses_list.append(course.course.course_code)

    if not request.user.is_authenticated:
        raise Exception(DisallowedRedirect)

    if request.method == 'POST':
        grades = request.POST.getlist('course_grade')

        for i in range(len(program_courses)):
            if grades[i] is not "":
                found = False

                for taken in courses_taken:
                    if taken.course_id == program_courses_list[i]:
                        found = True
                        StudentCourses.objects.filter(id=taken.id).update(course_grade=grades[i])
                if not found:
                    new_course = StudentCourses.objects.create(course_grade=grades[i], student=Students.objects.filter(student_user=request.user.id)[0],
                                                               course_id=program_courses_list[i])
                    new_course.save()

        if submit_button is not None:
            return redirect('/curriculum')

    else:
        form = Curriculum_Form()

    if request.user.students.student_program == "ICOM":
        return render(request, 'UPR_Grader/icom_curriculum.html', {'form': form, 'program_courses': program_courses, 'courses_taken': courses_taken})

    elif request.user.students.student_program == "CIIC" or request.user.students.student_program == "INSO":
        return render(request, 'UPR_Grader/coming_soon.html')

    elif request.user.students.student_program == "INEL":
        return render(request, 'UPR_Grader/inel_curriculum.html', {'form': form, 'program_courses': program_courses, 'courses_taken': courses_taken})

    else:
        return render(request, 'UPR_Grader/no_academic_program.html')
