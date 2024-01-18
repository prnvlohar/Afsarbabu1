
from django.urls import path

from assessment.views import (AddAssessmentView,
                              AddQuestionView, QuestionDeleteView,ListAssessment,
                              QuestionListView, QuestionUpdateView,
                              ShowAssessmentView, ShowQuizView, rating_quiz, TopicListView,
                              SubTopicListView, AssessmentListView, QuestionListView,
                              AssessmentUpdateView, AddSubtopicView, UpdateSubtopicView,
                              AddTopicView, UpdateTopicView, QuestionDeleteView, AssessmentDeleteView,
                              SubtopicDeleteView, TopicDeleteView)

urlpatterns = [
    path('show-assessment/', ShowAssessmentView.as_view(), name='show-assessment'),
    path('add-question/<pk>/', AddQuestionView.as_view(), name='add-question'),
    # question crud
    path('show-question/', QuestionListView.as_view(), name='show-question'),

    path('update-question/<int:pk>/',
         QuestionUpdateView.as_view(), name='update-question'),
    # path('quiz/', QuizView.as_view(), name = 'quiz'),
    # path('text-quiz/', TextquizView.as_view(), name = 'text_quiz'),
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
    path('delete-topic/<int:pk>/', TopicDeleteView.as_view(), name = "delete-topic")
    
    
]
