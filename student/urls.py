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
     path("", views.index, name="StudentHome"),
     path("signup",views.signup,name="signup"),
     path("login2",views.login2,name="login2"),
     path("studentlogin",views.studentlogin,name="login"),
     path("handlelogin",views.handlelogin,name="handlelogin"),
     path("studentlogout",views.studentlogout,name="studentlogout"),
     path("attemptQuiz",views.attemptQuiz,name="attemptQuiz"),
     path("handleAttemptQuiz",views.handleAttemptQuiz,name="handleAttemptQuiz"),
     path("choosePaper",views.choosePaper,name="choosePaper"),
     path("viewProfile",views.viewProfile,name="viewProfile"),
     path("studentLibrary",views.studentLibrary,name="studentLibrary"),
     path("updateProfilePic",views.updateProfilePic,name="updateProfilePic"),
     path("handleUpdateProfilePic",views.handleUpdateProfilePic,name="handleUpdateProfilePic"),
     path("liveExams",views.liveExams,name="liveExams"),
     path("liveAttemptQuiz",views.liveAttemptQuiz,name="liveAttemptQuiz"),
     path("handleLiveAttemptQuiz",views.handleLiveAttemptQuiz,name="handleLiveAttemptQuiz"),
     path("leaderBoard",views.leaderBoard,name="leaderBoard"),
     path("handleLeaderBoard",views.handleLeaderBoard,name="handleLeaderBoard"),
     path("studentpage",views.studentpage,name="StudentPage"),
     
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

