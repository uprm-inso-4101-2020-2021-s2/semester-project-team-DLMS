# Generated by Django 3.1.6 on 2021-04-02 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UPR_Grader', '0008_auto_20210402_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolled_courses',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='UPR_Grader.students'),
        ),
    ]
