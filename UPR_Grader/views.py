from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from .models import Students
from .backends import StudentsBackend
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def register_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']

        # Hashing the student's password
        hashed_password = make_password(password1)

        # Inserting student data to UPR_Grader_DB
        student_data = Students.objects.create(student_first_name=first_name, student_last_name=last_name,
                                               student_email=email, student_password=hashed_password)

        return render(request, 'UPR_Grader/home.html')

    return render(request, 'UPR_Grader/register.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = StudentsBackend.authenticate(request, email=email, password=password)
        print(email, password)
        print(user)

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.BaseBackend')
            return render(request, 'UPR_Grader/home.html')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect("/")

    return render(request, 'UPR_Grader/login.html', )


def home_page(request):
    return HttpResponse("WELCOME HOME")
