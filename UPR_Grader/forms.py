from django.forms import ModelForm
from .models import Enrolled_Courses


class Enrolled_CoursesForm(ModelForm):
    class Meta:
        model = Enrolled_Courses
        fields = ['course_code', 'course_title', 'course_credits']
