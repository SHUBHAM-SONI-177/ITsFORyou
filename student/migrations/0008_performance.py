# Generated by Django 3.0.4 on 2020-04-25 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_studymaterial'),
    ]

    operations = [
        migrations.CreateModel(
            name='performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentID', models.EmailField(max_length=254)),
                ('paperID', models.CharField(max_length=200)),
                ('time', models.DateTimeField()),
                ('percentageMarks', models.IntegerField()),
            ],
        ),
    ]
