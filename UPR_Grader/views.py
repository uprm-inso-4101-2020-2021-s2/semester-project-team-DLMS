from django.shortcuts import render
from UPR_Grader.models import Students
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'UPR_Grader/register.html', context)


def login_page(request):
    context = {}
    return render(request, 'UPR_Grader/login.html', context)
