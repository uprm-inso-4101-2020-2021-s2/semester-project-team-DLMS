from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from .models import Students
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.db import *

# Create your views here.
def register_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Hashing the student's password
        # hashed_password = make_password(password1)

        # Inserting student data to UPR_Grader_DB
        # Students.objects.create(student_first_name=first_name, student_last_name=last_name, student_email=email,
        #                         student_password=hashed_password)

        if password1 == password2:
            try:
                user = User.objects.create_user(username=email, email=email, password=password1, first_name=first_name,
                                                last_name=last_name)
                user.save()

                return render(request, 'UPR_Grader/home.html')

            except IntegrityError:
                # CHANGE
                print("DUMB")

    return render(request, 'UPR_Grader/register.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'UPR_Grader/home.html')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect("/")

    return render(request, 'UPR_Grader/login.html', )


def home_page(request):
    return HttpResponse("WELCOME HOME")
