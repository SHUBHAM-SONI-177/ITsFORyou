# Generated by Django 3.0.4 on 2020-04-28 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_student_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profilePic',
            field=models.ImageField(default='default.png', upload_to=''),
        ),
    ]