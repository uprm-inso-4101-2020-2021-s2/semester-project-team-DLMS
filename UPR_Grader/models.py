from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Students(models.Model):
    student_campus = models.CharField(max_length=20, default='Mayaguez')
    student_program = models.CharField(max_length=20, default='ICOM')  # Replace later with program table foreign key(ManyToOne)
    student_user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    student_gpa = models.CharField(max_length=4, default=0.00)
    student_major_gpa = models.CharField(max_length=4, default=0.00)

class Courses(models.Model):
    course_credits = models.IntegerField()
    course_name = models.CharField(max_length=50)

class Program(models.Model):
    program_name = models.CharField(max_length=100)
    program_course_total = models.IntegerField()
    program_credits = models.IntegerField()
    program_department = models.CharField(max_length=100)

class StudentCourses(models.Model):
    course_grade = models.CharField(max_length=1)
    course_professor = models.CharField(max_length=50)
    course_is_concentration = models.BooleanField()
    course_time_start = models.TimeField()
    course_time_end = models.TimeField()
    course_section = models.CharField(max_length=10)
    course_semester = models.IntegerField()
    student = models.OneToOneField('Students', on_delete=models.CASCADE)
    course = models.OneToOneField('Courses', on_delete=models.CASCADE)

class Program_Courses(models.Model):
    program = models.OneToOneField('Program', on_delete=models.CASCADE)
    course = models.OneToOneField('Courses', on_delete=models.CASCADE)

class Enrolled_Courses(models.Model):
    course_code = models.CharField(max_length=9)
    course_title = models.CharField(max_length=100)
    course_credits = models.CharField(max_length=2)
    student = models.OneToOneField('Students', on_delete=models.CASCADE)




