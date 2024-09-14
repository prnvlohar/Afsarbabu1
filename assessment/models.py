
from django.db import models

from users.models import CustomUser
from django.core.exceptions import ValidationError
# Create your models here.

class Topic(models.Model):

    title = models.CharField(max_length=100, null = True)

    def __str__(self):
        return self.title

class Subtopic(models.Model):
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=100, null = True)
    
    def __str__(self):
        return self.title
    
class Exams(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="exams_images/",null = True)
    
    def __str__(self):
        return self.name
    
    
class Assessment(models.Model):

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null = True)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, null = True)
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=100, null = True)
    duration = models.DurationField(null = True)

    @property
    def no_of_questions(self):
        return Question.objects.filter(assessment=self).count()
    
    def __str__(self):
        return f"{self.topic} - {self.subtopic} - {self.title}"

class Question(models.Model):

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    no = models.IntegerField(null=True, blank=True)
    question = models.CharField(max_length=1024, null=True)
    images = models.ImageField(upload_to="images/", null = True, blank=True)
    option1 = models.CharField(max_length=1024, null=True)
    option2 = models.CharField(max_length=1024, null=True)
    option3 = models.CharField(max_length=1024, null=True)
    option4 = models.CharField(max_length=1024, null=True)
    answer = models.CharField(max_length=1024, null=True)
    explanation = models.CharField(max_length=2024, null=True)
    
    @property
    def correct_answer_alias(self):
        if self.answer == self.option1:
            return "A"
        elif self.answer == self.option2:
            return "B"
        elif self.answer == self.option3:
            return "C"
        elif self.answer == self.option4:
            return "D"
        
    def __str__(self) -> str:
        return self.question
    
    class meta:
        unique_together = ('assessment', 'no')


class Rating(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.user} rated {self.rating} star for {self.assessment}'


class PassFailStatus(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    status = models.BooleanField()
    
    def __str__(self):
        return f'{self.user} - {self.assessment} - {self.status}'


class ResultAnalysis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    pass_fail_status = models.ForeignKey(PassFailStatus, on_delete=models.CASCADE, related_name='result_analysis')
    attempted = models.IntegerField()
    correct = models.IntegerField()
    questions_status = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    
    
    @property
    def formatted_created_at(self):
        print(self.created_at.strftime("%Y/%m/%d %H:%M"))
        return self.created_at.strftime("%Y/%m/%d %H:%M")
    @property
    def incorrect(self):
        return self.attempted - self.correct
    
    @property
    def percentage(self):
        """Calculates the percentage of correct answers."""
        if self.attempted > 0:
            percent = (self.correct / self.assessment.no_of_questions) * 100
            if percent>0:
                return round(percent, 2)
        return 0.1
    
    def __str__(self):
        return f'{self.assessment} - {self.pass_fail_status} - {self.attempted} - {self.correct}'

    # def clean(self):
    #     if self.pass_fail_status.user != self.user:
    #         raise ValidationError('Pass fail status does not belong to the user')
    #     if self.pass_fail_status.assessment != self.assessment:
    #         raise ValidationError('Pass fail status does not belong to the assessment')

    def save(self, *args, **kwargs):
        
        pass_or_fail = self.percentage >= 60
        
        if not self.pk: 
            self.pass_fail_status = PassFailStatus.objects.create(user=self.user, assessment=self.assessment, status=pass_or_fail)
        else:
            self.pass_fail_status.status = pass_or_fail
            self.pass_fail_status.save()

        super().save(*args, **kwargs)