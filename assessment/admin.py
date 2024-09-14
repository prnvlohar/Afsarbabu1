from django.contrib import admin
from .models import Topic, Subtopic, Exams, Assessment, Question, Rating, PassFailStatus, ResultAnalysis

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['title']
    list_display = ['title']
    ordering = ['title']

@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):
    search_fields = ['title', 'topic__title']
    list_filter = ['topic']
    list_display = ['title', 'topic']
    ordering = ['title', 'topic__title']

@admin.register(Exams)
class ExamsAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ['name']
    ordering = ['name']

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    search_fields = ['title', 'topic__title', 'subtopic__title', 'exam__name']
    list_filter = ['topic', 'subtopic', 'exam']
    list_display = ['title', 'topic', 'subtopic', 'exam', 'duration']
    ordering = ['title', 'topic__title', 'subtopic__title', 'exam__name']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question', 'assessment__title']
    list_filter = ['assessment']
    list_display = ['no','question', 'assessment']
    ordering = ['assessment__title', 'question']

@admin.register(PassFailStatus)
class PassFailStatusAdmin(admin.ModelAdmin):
    search_fields = [ 'assessment__title', 'status']
    list_filter = ['status', 'assessment']
    list_display = ['user', 'assessment', 'status']
    ordering = ['assessment__title', 'status']

admin.site.register(ResultAnalysis)
# Register all models not explicitly registered
