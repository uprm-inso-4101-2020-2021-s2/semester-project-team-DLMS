from django.db import models


# Create your models here.

class Students(models.Model):
    student_id = models.IntegerField()
    student_email = models.CharField(max_length=100)
    student_first_name = models.CharField(max_length=25)
    student_last_name = models.CharField(max_length=50)
