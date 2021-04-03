from django.forms import ModelForm
from .models import Enrolled_Courses
from django import forms

GRADES = [(None, ''), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')]


class Enrolled_CoursesForm(forms.Form):
    course_code = forms.CharField(max_length=20)
    course_title = forms.CharField(max_length=30)
    course_credits = forms.CharField(max_length=2)
    student = forms.HiddenInput()

class Edit_Form(ModelForm):
    class Meta:
        model = Enrolled_Courses
        fields = ['course_code', 'course_title', 'course_credits']

class Curriculum_Form(forms.Form):
    course_code = forms.HiddenInput()
    course_title = forms.HiddenInput()
    course_credits = forms.HiddenInput()
    course_grade = forms.ChoiceField(label='', choices=GRADES, required=False)




