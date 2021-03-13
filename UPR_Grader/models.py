from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Students(models.Model):
    student_campus = models.CharField(max_length=20, default='Mayaguez')
    student_program = models.CharField(max_length=20, default='ICOM')  # Replace later with program table foreign key(ManyToOne)
    student_user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    student_gpa = models.CharField(max_length=4, default=0.00)
    student_major_gpa = models.CharField(max_length=4, default=0.00)


class Enrolled_Courses(models.Model):
    course_code = models.CharField(max_length=9)
    course_title = models.CharField(max_length=100)
    course_credits = models.CharField(max_length=2)




