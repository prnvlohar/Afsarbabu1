
from django import forms

from assessment.models import Assessment, Question, Rating, Subtopic, Topic, Exams


class AssessmentForm(forms.ModelForm):

    class Meta:
        model = Assessment
        fields = ['title','duration']
        # widgets = {
        #     'duration' : forms.TextInput(attrs={'class':'durationInputWidget'})
        # }

class ExamForm(forms.ModelForm):

    class Meta:
        model = Exams
        fields = '__all__'

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        # fields = '__all__'
        exclude = ['assessment']


class SubtopicForm(forms.ModelForm):
    class Meta:
        model = Subtopic
        fields = ['title']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']

class RatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = '__all__'

        widgets = {
            'user': forms.HiddenInput(),
            'assessment': forms.HiddenInput(),
            'rating': forms.HiddenInput(),
        }
