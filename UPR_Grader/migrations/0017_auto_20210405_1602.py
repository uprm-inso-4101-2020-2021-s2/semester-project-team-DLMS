# Generated by Django 3.1.6 on 2021-04-05 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UPR_Grader', '0016_auto_20210405_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='student_gpa',
            field=models.CharField(default=0.0, max_length=4),
        ),
    ]
