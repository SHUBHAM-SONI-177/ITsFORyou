# Generated by Django 3.0.4 on 2020-04-28 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_performance'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='profilePic',
            field=models.ImageField(blank=True, default='default.jpeg', upload_to=''),
        ),
    ]
