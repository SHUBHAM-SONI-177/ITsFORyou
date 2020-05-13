from django.db import models

# Create your models here.
class faculty(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    dob=models.DateField()
    address=models.CharField(max_length=300)
    password=models.CharField(max_length=30,default='None')
    profilePic=models.ImageField(null=True)

    def __str__(self):
        return self.email
