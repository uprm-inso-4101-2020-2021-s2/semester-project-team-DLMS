from django.shortcuts import render, redirect
from UPR_Grader.models import Students
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import random
from django.contrib import auth
from django.contrib import messages
import psycopg2
from .models import Students

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

        # Inserting student data to UPR_Grader_DB
        student_data = Students.objects.create(student_first_name=first_name, student_last_name=last_name, student_email=email)

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
