
from django.urls import path

from assessment.views import (AddAssessmentView,
                              AddQuestionView, QuestionDeleteView,ListAssessment,
                              QuestionListView, QuestionUpdateView,
                              ShowAssessmentView, ShowQuizView, rating_quiz, TopicListView,
                              SubTopicListView, AssessmentListView, QuestionListView,
                              AssessmentUpdateView)

urlpatterns = [
    path('show-assessment/', ShowAssessmentView.as_view(), name='show-assessment'),
    path('add-question/<pk>/', AddQuestionView.as_view(), name='add-question'),
    # question crud
    path('show-question/', QuestionListView.as_view(), name='show-question'),
    path('delete-question/<int:pk>/',
         QuestionDeleteView.as_view(), name='delete-question'),
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
    
]
