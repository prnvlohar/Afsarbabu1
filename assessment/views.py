from typing import Any
from django.contrib import messages
from django.db.models import Avg
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.core import serializers
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.shortcuts import get_object_or_404
from assessment.forms import (AssessmentForm, QuestionForm, RatingForm, SubtopicForm, TopicForm, ExamForm)
from assessment.models import ( Assessment, Question,
                               Rating, PassFailStatus, Topic, Subtopic, Exams,
                               ResultAnalysis)
from assessment.utils import send_email_with_marks, get_option_alias
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.urls import reverse
from urllib.parse import urlencode
import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyBOW2L_bcv8mEtPBWT0ulVxC8ijUIFkkBk")

model = genai.GenerativeModel("gemini-1.5-flash")

import json
    



class TopicListView(LoginRequiredMixin, ListView):
    " Showing all topic present in project "
    model = Topic
    template_name = 'assessment/topic.html'
    context_object_name = "Topics"
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()


class SubTopicListView(LoginRequiredMixin, ListView):

    " Showing all topic present in project "
    model = Subtopic
    template_name = 'assessment/subtopic.html'
    context_object_name = "SubTopics"

    # overide method to send only that subtopic which belong to that topic
    def get_queryset(self):
        return Subtopic.objects.filter(topic=self.kwargs['pk'])

    def get_context_data(self, **kwargs: Any):
        p = super().get_context_data(**kwargs)
        p['id'] = self.kwargs['pk']
        return p


class AssessmentListView(LoginRequiredMixin, ListView):

    " Showing all assessment present in project "
    model = Assessment
    template_name = 'assessment/new_assessment.html'
    context_object_name = "Assessments"

    # overide method to send only that assessment which belong to that subtopic
    def get_queryset(self):
        return Assessment.objects.filter(subtopic=self.kwargs['pk'])

    def get_context_data(self, **kwargs: Any):
        p = super().get_context_data(**kwargs)
        p['id'] = self.kwargs['pk']
        topic_id = Subtopic.objects.get(id=self.kwargs['pk']).topic.id
        p['id1'] = topic_id
        return p


class QuestionListView(LoginRequiredMixin, ListView):

    model = Question
    template_name = "assessment/new_questions.html"
    context_object_name = "Questions"

    def get_queryset(self):
        # Filter questions based on assessment
        queryset = Question.objects.filter(assessment=self.kwargs['pk']).order_by('no')

        # Process queryset to truncate question_text without using annotate
        for question in queryset:
            question.short_question = question.question[:57] + '...' if len(
                question.question) > 60 else question.question

        return queryset

    def get_context_data(self, **kwargs: Any):
        p = super().get_context_data(**kwargs)
        p['id'] = self.kwargs['pk']
        p['id1'] = Assessment.objects.get(id=self.kwargs['pk']).subtopic.id
        return p

    def post(self, request, *args, **kwargs):
        assessment = Assessment.objects.get(id=kwargs['pk'])
        redirect_url = reverse('question-list', kwargs={'pk': kwargs['pk']})

        # Handle the uploaded JSON file
        if 'json_file' in request.FILES:
            json_file = request.FILES['json_file']
            try:
                # Assuming the JSON file contains a list of assessments
                assessments_data = json.load(json_file)
                for i in assessments_data:
                    question = i['question']
                    option1 = i['options'][0]
                    option2 = i['options'][1]
                    option3 = i['options'][2]
                    option4 = i['options'][3]
                    answer = i['answer']
                    explanation = i.get('explanation', None)
                    Question.objects.create(assessment=assessment, question=question, option1=option1,
                                            option2=option2, option3=option3, option4=option4, answer=answer, explanation=explanation)
                messages.success(request, 'Questions added successfully.')

            except:
                return_url = urlencode(
                    {'error': 'Invalid JSON file, format of json file provided by you is not valid please check that you miss something'})
                redirect_url = f'{redirect_url}?{return_url}'

        return redirect(redirect_url)


class ListAssessment(LoginRequiredMixin, View):

    " Showing all assessment present in project "

    template_name = 'assessment/list_assessment.html'

    def get(self, request, *args, **kwargs):
        assessment = Assessment.objects.all()
        return render(request, self.template_name, {'assessment': assessment, })


class ShowAssessmentView(LoginRequiredMixin, View):

    " Showing all assessment present in project "

    template_name = 'assessment/assessment.html'

    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            q = request.GET['q']
            assessment = Assessment.objects.filter(title__icontains=q)
        else:
            assessment = Assessment.objects.all()
        assessment = assessment.annotate(
            avg_rating=Avg('rating__rating', default=0))
        return render(request, self.template_name, {'assessment': assessment, })


class AddQuestionView(LoginRequiredMixin, View):

    " Adding questions for assessment "

    form_class = QuestionForm
    template_name = "assessment/addQuestion.html"

    def get(self, request, *args, **kwargs):
        assessment_id = kwargs.get('pk')
        assessment = get_object_or_404(Assessment, id=assessment_id)
        count = Question.objects.filter(assessment=assessment).count()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'count': count, 'assessment': assessment, 'id': self.kwargs['pk']})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        user = request.user

        if user.type == 'instructor':
            if form.is_valid():
                assessment_id = kwargs.get('pk')
                assessment = get_object_or_404(Assessment, id=assessment_id)
                # insert assessment in form data
                form.instance.assessment = assessment
                form.save()
                messages.error(request, 'Question added successfully.')
                # return reverse of add-question with assessemnt id
                return HttpResponseRedirect(reverse('add-question', args=[assessment_id]))
            else:
                messages.error(request, 'Question add failed.')
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'User is not instructor.')
            return HttpResponseRedirect(reverse('index'))


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = "assessment/question_confirm_delete.html"

    def get_success_url(self) -> str:
        assessment_id = self.object.assessment.id
        success_url = f"/assessment/qestion-list/{assessment_id}/"
        return success_url


class AssessmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Assessment
    template_name = "assessment/question_confirm_delete.html"

    def get_success_url(self) -> str:
        # add assessment id to success url
        subtopic_id = self.object.subtopic.id
        success_url = f"/assessment/assessment-list/{subtopic_id}/"
        return success_url


class SubtopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Subtopic
    template_name = "assessment/question_confirm_delete.html"

    def get_success_url(self) -> str:
        # add assessment id to success url
        subtopic_id = self.object.topic.id
        success_url = f"/assessment/sub-topic-list/{subtopic_id}/"
        return success_url


class TopicDeleteView(LoginRequiredMixin, DeleteView):
    model = Topic
    success_url = '/assessment/topic-list'
    template_name = "assessment/question_confirm_delete.html"


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['no','question','images', 'option1', 'option2', 'option3', 'option4', 'answer','explanation']
    template_name = "assessment/question_confirm_update.html"

    def form_valid(self, form):
        # Get the current question object and its assessment
        question = self.get_object()
        current_no = question.no
        new_no = form.cleaned_data['no']
        assessment = question.assessment

        # Handle the reordering if the question number is changed
        if current_no != new_no:
            # If the new number is less than the current number, increment questions in the range
            if new_no < current_no:
                Question.objects.filter(
                    assessment=assessment,
                    no__gte=new_no,
                    no__lt=current_no
                ).update(no=F('no') + 1)

            # If the new number is greater than the current number, decrement questions in the range
            else:
                Question.objects.filter(
                    assessment=assessment,
                    no__gt=current_no,
                    no__lte=new_no
                ).update(no=F('no') - 1)

        # Save the form with the updated data
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        # add assessment id to success url
        assessment_id = self.object.assessment.id
        success_url = f"/assessment/qestion-list/{assessment_id}/"
        return success_url

    def get_context_data(self, **kwargs: Any):
        p = super().get_context_data(**kwargs)
        p['id'] = self.kwargs['pk']
        p['id1'] = Question.objects.get(id=self.kwargs['pk']).assessment.id
        return p


class AssessmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Assessment
    fields = ['title', 'duration', 'is_active']
    template_name = "assessment/update_assessment.html"

    def get_success_url(self) -> str:
        # add assessment id to success url
        assessment_id = self.object.id
        success_url = f"/assessment/assessment-list/{assessment_id}/"
        return success_url

    def get_context_data(self, **kwargs: Any):
        p = super().get_context_data(**kwargs)
        p['id'] = self.kwargs['pk']
        return p


class AddAssessmentView(LoginRequiredMixin, CreateView):
    form_class = AssessmentForm
    template_name = 'assessment/addassessment.html'

    def get_success_url(self) -> str:
        # add assessment id to success url
        assessment_id = self.object.subtopic.id
        success_url = f"/assessment/assessment-list/{assessment_id}/"
        return success_url

    # overrirde create method to add field manually
    def save(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().save(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.subtopic_id = self.kwargs.get('pk')
        topic_id = Subtopic.objects.get(id=self.kwargs.get('pk')).topic.id
        form.instance.topic_id = topic_id
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any):
        p = super().get_context_data(**kwargs)
        p['id'] = self.kwargs['pk']
        return p


class AddSubtopicView(LoginRequiredMixin, CreateView):
    form_class = SubtopicForm
    template_name = 'assessment/addsubtopic.html'

    def get_success_url(self) -> str:
        # add assessment id to success url
        subtopic_id = self.object.topic.id
        success_url = f"/assessment/sub-topic-list/{subtopic_id}/"
        return success_url

    def form_valid(self, form):
        topic = Topic.objects.get(id=self.kwargs.get('pk'))
        form.instance.topic = topic
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any):
        p = super().get_context_data(**kwargs)
        p['id'] = self.kwargs['pk']
        return p


class UpdateSubtopicView(LoginRequiredMixin, UpdateView):
    model = Subtopic
    fields = ['title']
    template_name = 'assessment/update_subtopic.html'

    def get_success_url(self) -> str:
        # add assessment id to success url
        subtopic_id = self.object.topic.id
        success_url = f"/assessment/sub-topic-list/{subtopic_id}/"
        return success_url

    def get_context_data(self, **kwargs: Any):
        p = super().get_context_data(**kwargs)
        p['id'] = self.kwargs['pk']
        return p


class AddTopicView(LoginRequiredMixin, CreateView):
    form_class = TopicForm
    template_name = 'assessment/add_topic.html'
    success_url = '/assessment/topic-list'


class UpdateTopicView(LoginRequiredMixin, UpdateView):
    model = Topic
    fields = ['title']
    template_name = 'assessment/update_topic.html'
    success_url = '/assessment/topic-list'

    def get_context_data(self, **kwargs: Any):
        p = super().get_context_data(**kwargs)
        p['id'] = self.kwargs['pk']
        return p


def guidelines(request, pk):
    return render(request, 'assessment/guidelines.html', context={'id': pk})


class TestShow(View):
    queryset = Question.objects.all()

    def get(self, request, *args, **kwargs):

        context = {
            'questions': self.queryset.filter(assessment=self.kwargs['pk']),
            'assessment': Assessment.objects.get(id=self.kwargs['pk'])
        }
        return render(request, 'assessment/test.html', context)

    def post(self, request, *args, **kwargs):
        queryset = self.queryset.filter(assessment=self.kwargs['pk']).order_by('no')
        
        total_attempted = len(request.POST)-1
        correct_ans = 0
        questions_status = {}
        for i in queryset:
            questions_status[i.id] = get_option_alias(request.POST.get(str(i.id), None),i)
            if i.answer == request.POST.get(str(i.id), None):
                correct_ans += 1
        
        result = ResultAnalysis.objects.create(
            user=request.user, assessment=Assessment.objects.get(id=self.kwargs['pk']),
            attempted=total_attempted, correct=correct_ans,
            questions_status=questions_status
        )
        
        return redirect(reverse('result', kwargs={'pk': result.id}))


def result(request, pk):
    result = ResultAnalysis.objects.get(id=pk)
    answer_key_url = reverse('answer-key', kwargs={'pk': pk})
    context = {
        'result': result,
        'answer_key_url':answer_key_url,
    }
    questions = Question.objects.filter(assessment=result.assessment.id).order_by('no')
    question_data = []
    for i in questions:
        question_data.append({
            'id': i.id,
            'question': f'{i.question[:25]+"..." if len(i.question) > 25 else i.question}',
            'option1': i.option1,
            'option2': i.option2,
            'option3': i.option3,
            'option4': i.option4,
            'correct_answer_alias': i.correct_answer_alias,
            'explanation': i.explanation,
            'correct_or_not': result.questions_status[str(i.id)]==i.correct_answer_alias,
            'answer_given': result.questions_status[str(i.id)]
        })
        
    context['question_data'] = question_data
    return render(request, 'assessment/result.html', context)


class ExamsListView(ListView):
    model = Exams
    template_name = 'assessment/exams_list.html'
    
class ExamAddView(View):
    def get(self, request, *args, **kwargs):
        form = ExamForm()
        context = {
            'form':form,
        }
        return render(request, 'assessment/add_exam.html', context)
    def post(self, request, *args, **kwargs):
        form = ExamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('exams')
        context = {
            'form':form,
            'error': 'Something went wrong either name or image is not valid'
        }
        return render(request, 'assessment/add_exam.html', context)
    

class ExamAssessmentListView(View):
    def get(self, request, *args, **kwargs):
        assessment = Assessment.objects.filter(exam__id=kwargs['pk'])
        return render(request, 'assessment/exams_assessment.html', {'Assessments':assessment})

def search_elasticsearch(request):
    query = request.GET.get("query", None)
    queryset_topic = Topic.objects.all()
    queryset_assessment = Assessment.objects.all()
    if query:
        queryset_topic = queryset_topic.filter(title__icontains=query)
        queryset_assessment = queryset_assessment.filter(title__icontains=query)
    topic_results = [{"id": item.id, "name": item.title} for item in queryset_topic]
    assessment_result = [{"id": item.id, "name": item.title, "subtopic": item.subtopic.title if item.subtopic else ''} for item in queryset_assessment]
    results = {
        "topic": topic_results,
        "assessment": assessment_result
    }
    return JsonResponse({"results": results})

def get_latest_5_results(request):
    results = ResultAnalysis.objects.filter(user = request.user).order_by('-created_at')
    if results:
        if len(results) > 5:
            results = results[:5]
        else:
            results = results
    data = []
    for result in results[::-1]:
        data.append({
            'created_at': result.formatted_created_at,
            'percentage': result.percentage
        })
    
    return JsonResponse(data, safe=False)


def answer_key_page(request, pk):
    result = ResultAnalysis.objects.get(id=pk)
    context = {
        'result': result
    }
    questions = Question.objects.filter(assessment=result.assessment.id).order_by('no')
    question_data = []
    for i in questions:
        question_data.append({
            'id': i.id,
            'question': i.question,
            'option1': i.option1,
            'option2': i.option2,
            'option3': i.option3,
            'option4': i.option4,
            'correct_answer_alias': i.correct_answer_alias,
            'explanation': str(i.explanation),
            'correct_or_not': result.questions_status[str(i.id)]==i.correct_answer_alias,
            'answer_given': result.questions_status[str(i.id)]
        })
        
    context['question_data'] = question_data
    return render(request, 'assessment/answer_key.html', context)


class ResultListView(ListView):
    model = ResultAnalysis
    template_name = 'assessment/result_list.html'
    context_object_name = 'results'
    
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(user=self.request.user)