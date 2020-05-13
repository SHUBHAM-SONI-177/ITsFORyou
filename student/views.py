from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import student
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth import login
from .models import question
from .models import performance
from datetime import datetime,timedelta,date
from .models import studyMaterial
from .models import paperTime
from .models import liveQuestionPaper
from .models import liveTestPerformance
from django.db.models import query_utils,query,Q
from passlib.hash import pbkdf2_sha256

wrongEmail=False
WrongPass=False
slogin=False
flogin=False
alogin=False
loggedin=False
loguser='None'
params={'slogin':False,'flogin':False,'alogin':False,'loggedin':False,'loguser':'None'}
def index(request):
    global params
    return render(request,'student/index.html',params)
def signup(request):
    global params
    if not params['loggedin'] :
        global wrongEmail
        global WrongPass
        if wrongEmail==True:
            wrongEmail=False
            params['flag2']:True
            return render(request,'student/signup.html',params)

        elif WrongPass==True:
            params['flag']=True
            return render(request,'student/signup.html',params)
        return render(request,'student/signup.html',params)
    else:
        return HttpResponseRedirect('/',params)

def handlelogin(request):
     global params
     temail=request.POST.get('email')
     tpassword=request.POST.get('password')
     user = authenticate(username=temail, password=tpassword)
     try:
         details=student.objects.get(email=temail)
     except:
         messages.error(request, 'wrong credentials')
         return HttpResponseRedirect('studentlogin',params)
     print(details.dob)
     if  pbkdf2_sha256.verify(tpassword,details.password):
         params['loggedin']=True
         params['slogin']=True
         params['loguser']=temail
         #login(request,user)
         messages.success(request, 'You are logged in succesfully')
         return HttpResponseRedirect('studentpage',params)
     else:
         messages.error(request, 'wrong credentials')
         return HttpResponseRedirect('studentlogin',params)
def studentlogin(request):
    global params
    if params['loggedin']==True:
        return HttpResponseRedirect('studentpage',params)
    return render(request,'student/login.html',params)
     

def login2(request):
    global params
    global wrongEmail
    global WrongPass
    print("yor are in login2")
    tname=request.POST.get('name','none')
    temail=request.POST.get('email','none')
    tdob=request.POST.get('dob','none')
    taddress=request.POST.get('address','none')
    tpassword=request.POST.get('password','none')
    trepeat_password=request.POST.get('repeat_password','none')
    tprofilepic=request.FILES.get('profilePic','none')
    
    test=student.objects.filter(email=temail)
    if len(test)!=0:
        wrongEmail=True
        messages.error(request, 'User already exist with this email')
        return HttpResponseRedirect('signup',params)
        
    #print(tname)
    #print(temail)
    #print(taddress)
    #print(tpassword)
    #print(trepeat_password)
    if trepeat_password==tpassword:
        enc_string=pbkdf2_sha256.encrypt(tpassword,rounds=12000,salt_size=32)
        tstudent=student(name=tname,email=temail,dob=tdob,address=taddress,password=enc_string,profilePic=tprofilepic)
        tstudent.save()
        #tuser = User.objects.create_user(username=temail,email=temail,password=tpassword)
        #tuser.save()                             
    else:
        WrongPass=True
        messages.error(request, 'passowrd did not match')
        return HttpResponseRedirect('signup',params)
    return HttpResponseRedirect('studentlogin',params)

def studentlogout(request):
    global params
    params['slogin']=False
    params['loggedin']=False
    params['loguser']='None'
    return HttpResponseRedirect('/',params)
def attemptQuiz(request):
    global params
    if request.method=="POST" :
        if params['slogin']:
            value=request.POST.get('paperID')
            q=question.objects.filter(paperID=value)
            print("it is me")
            try:
                print("itsm me1")
                q1=liveQuestionPaper.objects.get(paperID=value)
                
                currentTime=datetime.now()
                qtime=q1.quizTime
                qdate=q1.paperDate
                print(qtime)
                newdateTime=datetime.combine(qdate,qtime)
                newdateTime=newdateTime+timedelta(hours=5)
                if currentTime<newdateTime:
                    tempmessage="you can attempt this paper after"
                    tempmessage=tempmessage+newdateTime.strftime("%b %d %Y %H:%M")
                    print(tempmessage)
                    messages.error(request,tempmessage)
                    return HttpResponseRedirect("choosePaper",params)
            except:
                pass
            params['q']=q
            params['paperID']=value
            try:
                obj=paperTime.objects.get(paperID=value)
                params['ashu_time']=obj.quizTime
            except:
                params['ashu_time']=60

            
            return render(request,"student/attemptQuiz.html",params)
        else:
            messages.error(request, ' please log in In roder to attempt quiz')
            return HttpResponseRedirect('studentlogin',params)
    else:
        messages.error(request, 'first you should choose paper then only you can access the the quiz')
        return HttpResponseRedirect('studentpage',params)


def handleAttemptQuiz(request):
    global params
    if request.method=='POST':
        q=params.get('q').values()
        total=0
        right=0
        r1=0
        t1=0
        for obj in q:
            name=obj['questionText']
            value=request.POST.get(name)
            print(name)
            t1=t1+1
            total=total+obj['questionMarks']
            if value==obj['rightOption']:
                right=right+obj['questionMarks']
                r1=r1+1
                print("you are goddamn right")
            else:
                print("you are wrong")
        percentage=right/total
        percentage=percentage*100
        try:
            print("before1")
            print(params['paperID'])
            newp=performance.objects.get(paperID=params['paperID'],studentID=params['loguser'])
            print("brfor2")
            if(newp.percentageMarks<percentage):
                newp.percentageMarks=percentage
                newp.save()
        except:
            print("brfor3")
            newp=performance(studentID=params['loguser'],paperID=params['paperID'],time=datetime.now(),percentageMarks=percentage)
            newp.save()
        params['marks']=percentage
        params['rightQuestion']=r1
        params['totalQuestion']=t1
        return render(request,"student/result.html",params)
    else:
        return HttpResponse("invalid access")
def choosePaper(request):
    global params
    if params['slogin']:
        paperID=question.objects.values_list('paperID',flat=True).distinct()
        params['paperID']=paperID
        print("here i am")
        print(paperID)
        return render(request,"student/choosePaper.html",params)
    else:
        messages.error(request, 'first you should choose paper then only you can access the the quiz')
        return HttpResponseRedirect('/student',params)

def viewProfile(request):
    if params['slogin']:
        profile= student.objects.get(email=params['loguser'])
        studentPerformance=performance.objects.filter(studentID=params['loguser'])
        params['profile']=profile
        params['stp']=studentPerformance
        return render(request,"student/profile.html",params)
    else:
        messages.error(request, 'first you should login to view your profile')
        return HttpResponseRedirect('studentlogin',params)

def studentLibrary(request):
    global params
    if params['slogin']:
        books=studyMaterial.objects.all()
        params['books']=books
        return render(request,"student/studentLibrary.html",params)
    else:
        messages.error(request, 'first you should login to access study material')
        return HttpResponseRedirect('studentlogin',params)


def updateProfilePic(request):
     if request.method=='POST':
         if params['slogin']:
             return render(request,"student/updateProfilePic.html",params)
         else:
             messages.error(request,"please login to update profile")
             return HttpResponseRedirect('studentlogin',params)
    

def handleUpdateProfilePic(request):
    if request.method=='POST':
        if params['loggedin']:
            tprofilepic=request.FILES.get("profilePic",None)
            profile= student.objects.get(email=params['loguser'])
            profile.profilePic=tprofilepic
            profile.save()
            return HttpResponseRedirect('viewProfile',params)
        else:
            messages.error(request,"please login to update profile")
            return HttpResponseRedirect('studentlogin',params)
def liveExams(request):
    global params
    if params['slogin']:
        cdate=date.today()
        
        paperID1=liveQuestionPaper.objects.all()
        print(paperID1)
        paperID2=[]
        fdate=[]
        for obj in paperID1:
            newtime=datetime.combine(obj.paperDate,obj.quizTime)
            obj21=paperTime.objects.get(paperID=obj.paperID)
            enddatetime=newtime+timedelta(minutes=obj21.quizTime)
            if newtime>datetime.now() or (datetime.now()>newtime and datetime.now()<enddatetime):
                paperID2.append(obj)
        
                
        if len(paperID2)==0:
            return HttpResponse("there are not any live exams")
        params['paperID']=paperID2
        
        print("here i am")
      
        return render(request,"student/liveExams.html",params)
    else:
        messages.error(request, 'first you should choose paper then only you can access the the quiz')
        return HttpResponseRedirect('studentpage',params)
    
def liveAttemptQuiz(request):
    global params
    if request.method=="POST" :
        if params['slogin']:
            value=request.POST.get('paperID')
            q=question.objects.filter(paperID=value)
            print("itsm me")
            try:
                print("itsm me1")
                q1=liveQuestionPaper.objects.get(paperID=value)
                
                currentTime=datetime.now()
                qtime=q1.quizTime
                qdate=q1.paperDate
                newdateTime=datetime.combine(qdate,qtime)
                obj21=paperTime.objects.get(paperID=value)
                enddatetime=newdateTime+timedelta(minutes=obj21.quizTime)
                if currentTime<newdateTime or currentTime>enddatetime:
                    tempmessage="you can attempt this paper after"
                    tempmessage=tempmessage+newdateTime.strftime("%b %d %Y %H:%M")
                    print(tempmessage)
                    messages.error(request,tempmessage)
                    return HttpResponseRedirect("choosePaper",params)
            except:
                pass
            params['q']=q
            params['ashu_paperID']=value
            params['paperID']=value
            try:
                obj=paperTime.objects.get(paperID=value)
                params['ashu_time']=obj.quizTime
            except:
                params['ashu_time']=60

            
            return render(request,"student/liveAttemptQuiz.html",params)
        else:
            messages.error(request, ' please log in In roder to attempt quiz')
            return HttpResponseRedirect('studentlogin',params)
    else:
        messages.error(request, 'first you should choose paper then only you can access the the quiz')
        return HttpResponseRedirect('studentpage',params)
def handleLiveAttemptQuiz(request):
    global params
    if request.method=='POST':

        q=params.get('q').values()
        total=0
        right=0
        r1=0
        t1=0
        for obj in q:
            name=obj['questionText']
            value=request.POST.get(name)
            print(name)
            t1=t1+1
            total=total+obj['questionMarks']
            if value==obj['rightOption']:
                right=right+obj['questionMarks']
                r1=r1+1
                print("you are goddamn right")
            else:
                print("you are wrong")
        percentage=right/total
        percentage=percentage*100
        newp=performance(studentID=params['loguser'],paperID=params['paperID'],time=datetime.now(),percentageMarks=percentage)
        newp.save()
        params['marks']=percentage
        params['rightQuestion']=r1
        params['totalQuestion']=t1
        tempobj=liveTestPerformance.objects.filter(studentID=params['loguser'])
        if len(tempobj)==0:
            newPerformance=liveTestPerformance(studentID=params['loguser'],paperID=params['ashu_paperID'],studentMarks=percentage)
            newPerformance.save()
            print(newPerformance)
        else:
            return HttpResponse("invalid access")    
        return render(request,"student/result.html",params)
    else:
        return HttpResponse("invalid access")
def leaderBoard(request):
    if params['slogin']:
        cdate=date.today()
        paperID1=liveQuestionPaper.objects.all()
        print(paperID1)
        paperID2=[]
        fdate=[]
        for obj in paperID1:
            newtime=datetime.combine(obj.paperDate,obj.quizTime)
            obj21=paperTime.objects.get(paperID=obj.paperID)
            enddatetime=newtime+timedelta(minutes=obj21.quizTime)
            if datetime.now()>enddatetime:
                paperID2.append(obj)
        
                
        if len(paperID2)==0:
            return HttpResponse("No data to show")
        params['paperID']=paperID2
        
      
        return render(request,"student/leaderBoard.html",params)
    else:
        messages.error(request, "please login")
        return HttpResponseRedirect('/student',params)
def handleLeaderBoard(request):
    global params
    if request.method=="POST" :
        if params['slogin']:
            value=request.POST.get('paperID')
            leaders=liveTestPerformance.objects.filter(paperID=value)
            leaders=leaders.values()
            if len(leaders)==0:
                return HttpResponse("No data to show")
            sorted(leaders,key=lambda i:i['studentMarks'],reverse=True)
            params['leaders']=leaders
            return render(request,"student/handleLeaderBoard.html",params)
        else:
            messages.error(request, ' please login in roder to attempt quiz')
            return HttpResponseRedirect('studentlogin',params)
    else:
        messages.error(request, 'first you should choose paper then only you can access the the leaderBoard')
        return HttpResponseRedirect('studentpage',params)

def studentpage(request):
    if params['slogin']:
        books=studyMaterial.objects.all()
        params['books']=books
        profile= student.objects.get(email=params['loguser'])
        studentPerformance=performance.objects.filter(studentID=params['loguser'])
        params['profile']=profile
        params['stp']=studentPerformance
        return render(request,"student/studentpage.html",params)
    else:
        messages.error(request, 'first you should login')
        return HttpResponseRedirect('studentlogin',params)