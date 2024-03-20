from django.contrib import admin

from assessment.models import Assessment, Question, Rating, PassFailStatus, Topic, Subtopic, Exams

# Register your models here.

admin.site.register(Assessment)
admin.site.register(Rating)
admin.site.register(PassFailStatus)
admin.site.register(Topic)
admin.site.register(Subtopic)
admin.site.register(Exams)
@admin.register(Question)
class questionadmin(admin.ModelAdmin):
    list_display = ('id','question')

