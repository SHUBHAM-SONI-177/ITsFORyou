from django.contrib import admin

# Register your models here.
from .models import student
from .models import question
from .models import studyMaterial
from .models import performance
from .models import paperTime
from .models import liveQuestionPaper
from .models import liveTestPerformance

admin.site.register(student)
admin.site.register(question)
admin.site.register(studyMaterial)
admin.site.register(performance)
admin.site.register(paperTime)
admin.site.register(liveQuestionPaper)
admin.site.register(liveTestPerformance)