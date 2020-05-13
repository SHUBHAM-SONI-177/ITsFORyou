"""examportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
     path("", views.index, name="FacultyHome"),
     path("questionInput", views.inputQuestion, name="inputQuestion"),
     path("uploadStudyMaterial", views.uploadStudyMaterial, name="uploadStudyMaterial"),
     path("signup",views.signup,name="signup"),
     path("login2",views.login2,name="login2"),
     path("facultylogin",views.facultylogin,name="login"),
     path("handlelogin",views.handlelogin,name="handlelogin"),
     path("facultylogout",views.facultylogout,name="facultylogout"),
     path("viewProfile",views.viewProfile,name="viewProfile"),
     path("updateProfilePic",views.updateProfilePic,name="updateProfilePic"),
     path("handleUpdateProfilePic",views.handleUpdateProfilePic,name="handleUpdateProfilePic"),
     path("setQuizTime",views.setQuizTime,name="setQuizTime"),
     path("handleSetQuizTime",views.handleSetQuizTime,name="handleSetQuizTime"),
     path("setLiveExamPaper",views.setLiveExamPaper,name="setLiveExamPaper"),
     path("handleSetLiveExamPaper",views.handleSetLiveExamPaper,name="handleSetLiveExamPaper"),
     path("facultypage",views.facultypage,name="facultypage"),
     path("seeQuestionPaper",views.seeQuestionPaper,name="seeQuestionPaper"),
     path("availblePaper",views.availblePaper,name="availblePaper"),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
