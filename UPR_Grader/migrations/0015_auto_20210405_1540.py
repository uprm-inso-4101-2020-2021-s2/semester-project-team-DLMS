# Generated by Django 3.1.6 on 2021-04-05 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPR_Grader', '0014_auto_20210405_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='student_major_gpa',
            field=models.CharField(default=0.0, max_length=1000),
        ),
    ]
