# Generated by Django 3.0.4 on 2020-03-23 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_remove_student_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(default='None', max_length=30),
        ),
    ]