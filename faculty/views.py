from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from student.models import question
from student.views import loggedin,loguser,params
from .forms import questionForm
from .forms import studyMaterialForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from .models import faculty
from student.models import paperTime
from student.models import liveQuestionPaper
from passlib.hash import pbkdf2_sha256

wrongEmail=False
WrongPass=False
slogin=False
flogin=False
alogin=False
loggedin=False
loguser='None'

def index(request):
    return render(request,'faculty/index.html',params)
def inputQuestion(request):
    if params['flogin']:
        form=questionForm(request.POST,request.FILES)
        if form.is_valid():
            paperID1=form.cleaned_data['paperID']
            paperTime.objects.get_or_create(paperID=paperID1)
            print("saved")
            form.save()
            form=questionForm()
        params['form']=form
        return render(request,'faculty/questionInput.html',params)
    else:
        messages.error(request, 'you have to login to upload queston paper')
        return HttpResponseRedirect('facultylogin',params)

def uploadStudyMaterial(request):
    if params['flogin']:
        form=studyMaterialForm(request.POST or None ,request.FILES or None)
        if form.is_valid():
            print("saved")
            form.save()
            form=studyMaterialForm()
        print("its not valid")
        params['form']=form
        return render(request,'faculty/uploadStudyMaterial.html',params)
    else:
        messages.error(request, 'you have to login to upload  study material')
        return HttpResponseRedirect('facultylogin',params)
        

def signup(request):
    global params
    if not params['loggedin'] :
        global wrongEmail
        global WrongPass
        if wrongEmail==True:
            wrongEmail=False
            params['flag2']:True
            return render(request,'faculty/signup.html',params)

        elif WrongPass==True:
            params['flag']=True
            return render(request,'faculty/signup.html',params)
        return render(request,'faculty/signup.html',params)
    else:
        messages.error(request, 'you are already signed in')
        return HttpResponseRedirect('/faculty',params)

def handlelogin(request):
     global params
     temail=request.POST.get('email')
     tpassword=request.POST.get('password')
     user = authenticate(username=temail, password=tpassword)
     try:
         details=faculty.objects.get(email=temail)
     except:
         messages.error(request, 'wrong credentials')
         return HttpResponseRedirect('facultylogin',params)
     if pbkdf2_sha256.verify(tpassword,details.password):
         params['loggedin']=True
         params['flogin']=True
         params['loguser']=temail
         #login(request,user)
         messages.success(request, 'You are logged in succesfully')
         return HttpResponseRedirect('facultypage',params)
     else:
         messages.error(request, 'wrong credentials')
         return HttpResponseRedirect('facultylogin',params)

def facultylogin(request):
    global params
    if params['loggedin']==True:
        return HttpResponseRedirect('facultypage',params)
    return render(request,'faculty/login.html',params)
     

def login2(request):
    global params
    global wrongEmail
    global WrongPass
    tname=request.POST.get('name','none')
    temail=request.POST.get('email','none')
    tdob=request.POST.get('dob','none')
    taddress=request.POST.get('address','none')
    tpassword=request.POST.get('password','none')
    trepeat_password=request.POST.get('repeat_password','none')
    tprofilepic=request.FILES.get('profilePic','none')
    
    test=faculty.objects.filter(email=temail)
    if len(test)!=0:
        wrongEmail=True
        return HttpResponseRedirect('signup',params)
        
    #print(tname)
    #print(temail)
    #print(taddress)
    #print(tpassword)
    #print(trepeat_password)
    if trepeat_password==tpassword:
        enc_string=pbkdf2_sha256.encrypt(tpassword,rounds=12000,salt_size=32)
        tstudent=faculty(name=tname,email=temail,dob=tdob,address=taddress,password=enc_string,profilePic=tprofilepic)
        tstudent.save()
        #tuser = User.objects.create_user(username=temail,email=temail,password=tpassword)
        #tuser.save()                             
    else:
        WrongPass=True
        return HttpResponseRedirect('signup',params)
    return HttpResponseRedirect('facultylogin',params)

def facultylogout(request):
    global params
    params['flogin']=False
    params['loggedin']=False
    params['loguser']='None'
    return HttpResponseRedirect('/',params)
def viewProfile(request):
    if params['flogin']:
        profile= faculty.objects.get(email=params['loguser'])
        params['profile']=profile
        return render(request,"faculty/profile.html",params)
    else:
        messages.error(request, 'first you should login to view your profile')
        return HttpResponseRedirect('facultylogin',params)


def updateProfilePic(request):
    if request.method=='POST':
        print("yes im in upadate profile pic")
        if params['flogin']:
            return render(request,"faculty/updateProfilePic.html",params)
        else:
            messages.error(request,"please login to update profile")
            return HttpResponseRedirect('facultylogin',params)

def handleUpdateProfilePic(request):
    if request.method=='POST':
        if params['flogin']:
            tprofilepic=request.FILES.get("profilePic",None)
            profile= faculty.objects.get(email=params['loguser'])
            profile.profilePic=tprofilepic
            profile.save()
            return HttpResponseRedirect('viewProfile',params)
        else:
            messages.error(request,"please login to update profile")
            return HttpResponseRedirect('facultylogin',params)
def setQuizTime(request):
    if params['flogin']:
        return render(request,'faculty/setQuizTime.html',params)
    else:
        messages.error(request,"please login to update profile")
        return HttpResponseRedirect('facultylogin',params)
def handleSetQuizTime(request):
    if params['flogin']:
        paperID1=request.POST.get("paperID")
        ashu_time=request.POST.get("ashu_time")
        try:
            obj = paperTime.objects.get(paperID=paperID1)
            obj.quizTime=ashu_time
            obj.save()
        except:
            messages.error(request,"paperTime updation failed")
            return HttpResponseRedirect('facultypage',params)
        messages.success(request,"paper time updated")
        return HttpResponseRedirect('facultypage',params)
    else:
        messages.error(request,"please login to set Quiz Time")
        return HttpResponseRedirect('facultylogin',params)

def setLiveExamPaper(request):
    if params['flogin']:
        return render(request,'faculty/setLiveExamPaper.html',params)
    else:
        messages.error(request,"please login to set Live Exam Paper")
        return HttpResponseRedirect('facultylogin',params)
        
def handleSetLiveExamPaper(request):
    if params['flogin']:
        paperID1=request.POST.get("paperID")
        ashu_time=request.POST.get("ashu_time")
        ashu_date=request.POST.get("ashu_date")
        try:
            print("check1")
            obj=liveQuestionPaper.objects.filter(paperID=paperID1)
            if len(obj)==0:
                ahsu_temp=liveQuestionPaper(paperID=paperID1,quizTime=ashu_time,paperDate=ashu_date)
                ahsu_temp.save()
            else:
                obj=liveQuestionPaper.objects.get(paperID=paperID1)
                
                obj.quizTime=ashu_time
                
                obj.paperDate=ashu_date
                
                obj.save()
        except:
            messages.error(request,"live paper settting failed")
            return HttpResponseRedirect('facultypage',params)
        messages.success(request,"live Question Paper Added")
        return HttpResponseRedirect('facultypage',params)
    else:
        messages.error(request,"please login to set Live Question Paperr")
        return HttpResponseRedirect('facultylogin',params)
    

def facultypage(request):
    if params['flogin']:
        profile= faculty.objects.get(email=params['loguser'])
        params['profile']=profile
        return render(request,"faculty/facultypage.html",params)
    else:
        messages.error(request, 'first you should login')
        return HttpResponseRedirect('facultylogin',params)

def availblePaper(request):
    global params
    if params['flogin']:
        paperID=question.objects.values_list('paperID',flat=True).distinct()
        params['paperID']=paperID
        print("here i am")
        print(paperID)
        return render(request,"faculty/availablePapers.html",params)
    else:
        messages.error(request, 'first you should login  then only you can see the the paper')
        return HttpResponseRedirect('facultylogin',params)
def seeQuestionPaper(request):
    global params
    if request.method=="POST" :
        if params['flogin']:
            value=request.POST.get('paperID')
            q=question.objects.filter(paperID=value)
            params['q']=q
            params['paperID']=value
            try:
                obj=paperTime.objects.get(paperID=value)
                params['ashu_time']=obj.quizTime
            except:
                params['ashu_time']=60

            return render(request,"faculty/seeQuestionPaper.html",params)
        else:
            messages.error(request, ' please log in In roder to attempt quiz')
            return HttpResponseRedirect('facultylogin',params)
    else:
        messages.error(request, 'first you should login then only you can see the questions')
        return HttpResponseRedirect('facultylogin',params)




