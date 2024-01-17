from django.contrib import admin

from assessment.models import Assessment, Question, Rating, PassFailStatus, Topic, Subtopic

# Register your models here.

admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(Rating)
admin.site.register(PassFailStatus)
admin.site.register(Topic)
admin.site.register(Subtopic)