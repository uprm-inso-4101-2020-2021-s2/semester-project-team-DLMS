from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
import random
from django.contrib import auth
from django.contrib import messages
from .models import Students
from passlib.hash import postgres_md5

# Create your views here.
def register_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']

        # Creating username with random number. This saves the user in Django's admin page.
        number = random.randint(0, 999)
        username = first_name + last_name + str(number)

        user = User.objects.create_user(first_name=first_name, last_name=last_name, password=password1, email=email,
                                        username=username)
        user.save()

        # Hashing the student's password
        hashed_password = postgres_md5.hash(str(password1), user=str(email))

        # Testing hashing
        # print(hashed_password)
        # print(email)
        # print(postgres_md5.verify(str(password1), hashed_password, user=str(email)))
        # print(postgres_md5.verify(str(password1), hashed_password, user="test@gmail.com"))

        # Inserting student data to UPR_Grader_DB
        student_data = Students.objects.create(student_first_name=first_name, student_last_name=last_name,
                                               student_email=email, student_password=hashed_password)

        return render(request, 'UPR_Grader/home.html')

    return render(request, 'UPR_Grader/register.html')


def login_page(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'UPR_Grader/home.html')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect("/")

    return render(request, 'UPR_Grader/login.html', )

def home_page(request):
    return HttpResponse("WELCOME HOME")
