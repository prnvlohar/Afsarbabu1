
from django import forms

from assessment.models import Assessment, Question, Rating, Subtopic, Topic


class AssessmentForm(forms.ModelForm):

    class Meta:
        model = Assessment
        fields = ['title','duration']
        # widgets = {
        #     'duration' : forms.TextInput(attrs={'class':'durationInputWidget'})
        # }


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
