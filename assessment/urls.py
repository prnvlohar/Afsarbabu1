
from django.urls import path

from assessment.views import (AddAssessmentView,
                              AddQuestionView, QuestionDeleteView,ListAssessment,
                              QuestionListView, QuestionUpdateView,
                              ShowAssessmentView, ShowQuizView, rating_quiz, TopicListView,
                              SubTopicListView, AssessmentListView, QuestionListView,
                              AssessmentUpdateView, AddSubtopicView, UpdateSubtopicView,
                              AddTopicView, UpdateTopicView, QuestionDeleteView, AssessmentDeleteView,
                              SubtopicDeleteView, TopicDeleteView, guidelines, TestShow, result, ExamsListView,
                              ExamAddView, ExamAssessmentListView, search_elasticsearch)

urlpatterns = [
    path('show-assessment/', ShowAssessmentView.as_view(), name='show-assessment'),
    path('add-question/<pk>/', AddQuestionView.as_view(), name='add-question'),
    path('show-question/', QuestionListView.as_view(), name='show-question'),
    path('update-question/<int:pk>/',
         QuestionUpdateView.as_view(), name='update-question'),
    path('show-quiz/<str:pk>/', ShowQuizView.as_view(), name='show-quiz'),
    path('rating/', rating_quiz, name='rating'),
    path('list-assessment',ListAssessment.as_view(),name='list-assessment'),
    
    path('topic-list',TopicListView.as_view(),name='topic-list'),
    path('sub-topic-list/<int:pk>/',SubTopicListView.as_view(),name='sub-topic-list'),
    path('assessment-list/<int:pk>/',AssessmentListView.as_view(),name='assessment-list'),
    path('qestion-list/<int:pk>/',QuestionListView.as_view(), name= "question-list"),
    path('update-assessment/<int:pk>/',AssessmentUpdateView.as_view(),name='update-assessment'),
    path('add-assessment/<int:pk>/', AddAssessmentView.as_view(), name='add-assessment'),
    path('add-subtopic/<int:pk>/', AddSubtopicView.as_view(), name='add_subtopic'),
    path('update-subtopic/<int:pk>/', UpdateSubtopicView.as_view(), name='update_subtopic'),
    path('add-topic/', AddTopicView.as_view(), name='add_topic'),
    path('update-topic/<int:pk>/', UpdateTopicView.as_view(), name='update_topic'),
    path('delete-question/<int:pk>/', QuestionDeleteView.as_view(), name = "delete-question"),
    path('delete-assessment/<int:pk>/', AssessmentDeleteView.as_view(), name = "delete-assessment"),
    path('delete-subtopic/<int:pk>/', SubtopicDeleteView.as_view(), name = "delete-subtopic"),
    path('delete-topic/<int:pk>/', TopicDeleteView.as_view(), name = "delete-topic"),
    path('guideline/<int:pk>/', guidelines, name = "guideline"),
    path('test/<int:pk>/', TestShow.as_view(), name = "test"),
    path('result/<int:pk>/', result, name = "result"),
    path('exams/', ExamsListView.as_view(), name = "exams"),
    path('exam-add/', ExamAddView.as_view(), name = "exam-add"),
    path('exam-assessment-list/<int:pk>/', ExamAssessmentListView.as_view(), name = "exam-assessment-list"),
    path('search-api',search_elasticsearch,name="search_api")
]
