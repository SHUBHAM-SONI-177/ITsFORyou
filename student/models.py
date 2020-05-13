from django.db import models
from datetime import datetime
# Create your models here.
class student(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    dob=models.DateField()
    address=models.CharField(max_length=300)
    password=models.CharField(max_length=1000,default='None')
    profilePic=models.ImageField(null=True)
   

    def __str__(self):
        return self.email
class question(models.Model):
    qid=models.AutoField(primary_key=True)
    paperID=models.CharField(max_length=100)
    questionTag=models.CharField(max_length=100)
    questionText=models.TextField()
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    rightOption=models.CharField(max_length=200)
    questionMarks=models.IntegerField(default=4)
    questionImage=models.ImageField(blank=True)
    class Meta:
        unique_together=('paperID','questionText',)

    def __str__(self):
        return str(self.qid)

class studyMaterial(models.Model):
    materialID=models.AutoField(primary_key=True)
    materialTag=models.CharField(max_length=200)
    title=models.CharField(max_length=200)
    materialFile=models.FileField()

class performance(models.Model):
    studentID=models.EmailField()
    paperID=models.CharField(max_length=200)
    time=models.DateTimeField()
    percentageMarks=models.IntegerField()
class paperTime(models.Model):
    paperID=models.CharField(max_length=100,primary_key=True)
    quizTime=models.IntegerField(default=60)
    def __str__(self):
        return self.paperID
class liveQuestionPaper(models.Model):
    paperID=models.CharField(max_length=100,primary_key=True)
    paperDate=models.DateField()
    quizTime=models.TimeField(default=datetime.now().time())
    def __str__(self):
        return self.paperID

class liveTestPerformance(models.Model):
    studentID=models.EmailField()
    paperID=models.CharField(max_length=100)
    studentMarks=models.IntegerField()
    def __str__(self):
        return self.studentID







