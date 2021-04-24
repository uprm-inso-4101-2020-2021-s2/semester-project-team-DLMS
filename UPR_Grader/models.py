from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Students(models.Model):
    student_campus = models.CharField(max_length=20, default='Mayaguez')
    student_program = models.CharField(max_length=20,
                                       default='ICOM')  # Replace later with program table foreign key(ManyToOne)
    student_user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    student_gpa = models.CharField(max_length=4, default=0.00)
    student_major_gpa = models.CharField(max_length=4, default=0.00)


class Courses(models.Model):
    course_credits = models.IntegerField()
    course_name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=50, unique=True)


class Program(models.Model):
    program_name = models.CharField(max_length=100, unique=True)
    program_course_total = models.IntegerField()
    program_credits = models.IntegerField()
    program_department = models.CharField(max_length=100)


class StudentCourses(models.Model):
    course_grade = models.CharField(max_length=1, default="-")
    course_professor = models.CharField(max_length=50, default="")
    course_is_concentration = models.BooleanField(default=False)
    # course_time_start = models.TimeField()
    # course_time_end = models.TimeField()
    course_section = models.CharField(max_length=10, default="005")
    student = models.ForeignKey('Students', on_delete=models.CASCADE)
    course = models.ForeignKey('Courses', to_field='course_code', on_delete=models.CASCADE)


class Enrolled_Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=9)
    course_title = models.CharField(max_length=100)
    course_credits = models.CharField(max_length=2)
    student = models.ForeignKey('Students', on_delete=models.CASCADE)


class Attendance(models.Model):
    course = models.ForeignKey('StudentCourses', on_delete=models.CASCADE)
    course_date = models.CharField(max_length=30)
    course_status = models.CharField(max_length=8)


class Grades(models.Model):
    course = models.ForeignKey('StudentCourses', on_delete=models.CASCADE)
    grade_name = models.CharField(max_length=30)  # Exam 1 or quiz 1
    grade_value = models.IntegerField()  # Value of the grade 0-100
    grade_char = models.CharField(max_length=1, default="-")  # A-F


class Program_Courses(models.Model):
    semester = models.IntegerField()
    program = models.ForeignKey('Program', to_field='program_name', on_delete=models.CASCADE)
    course = models.ForeignKey('Courses', to_field='course_code', on_delete=models.CASCADE)
