from django.forms import ModelForm
from .models import Enrolled_Courses
from django import forms

GRADES = [(None, ''), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')]
STATUS = [(None, ''), ('Present', 'Present'), ('Absent', 'Absent')]


class Enrolled_CoursesForm(forms.Form):
    id = forms.HiddenInput()
    course_code = forms.CharField(max_length=20)
    course_title = forms.CharField(max_length=30)
    course_credits = forms.CharField(max_length=2)
    student = forms.HiddenInput()


class AttendanceForm(forms.Form):
    id = forms.HiddenInput
    course = forms.HiddenInput
    course_date = forms.DateField(input_formats=['%d/%m/%Y'])
    course_status = forms.ChoiceField(label='Status', choices=STATUS, required=False)


class Edit_Form(ModelForm):
    class Meta:
        model = Enrolled_Courses
        fields = ['course_code', 'course_title', 'course_credits']


class GradesForm(forms.Form):
    course = forms.HiddenInput
    grade_name = forms.CharField(max_length=30)  # Exam 1 or quiz 1
    grade_value = forms.IntegerField()
    grade_char = forms.ChoiceField(label='Grade', choices=GRADES, required=False)


class Curriculum_Form(forms.Form):
    course_code = forms.HiddenInput()
    course_title = forms.HiddenInput()
    course_credits = forms.HiddenInput()
    course_grade = forms.ChoiceField(label='', choices=GRADES, required=False)
