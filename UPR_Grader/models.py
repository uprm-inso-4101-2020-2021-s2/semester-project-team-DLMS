from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Students(models.Model):
    #CAMPUS_CHOICES = ['Aguadilla', 'Arecibo', 'Bayamon', 'Carolina', 'Cayey', 'Ciencias Medicas', 'Humacao', 'Mayaguez', 'Ponce', 'Rio Piedras', 'Utuado']
    #PROGRAM_CHOICES = ['ICOM', 'INEL', 'INSO', 'CIIC']
    student_campus = models.CharField(max_length=20, default='Mayaguez')
    student_program = models.CharField(max_length=20, default='ICOM')  # Replace later with program table foreign key(ManyToOne)
    student_user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    student_gpa = models.CharField(max_length=4, default=0.00)
    student_major_gpa = models.CharField(max_length=4, default=0.00)
