
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
    
class Assessment(models.Model):

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null = True)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, null = True)
    title = models.CharField(max_length=100, null = True)
    duration = models.DurationField(null = True)

    def __str__(self):
        return self.title

class Question(models.Model):

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    question = models.CharField(max_length=1024, null=True)
    option1 = models.CharField(max_length=1024, null=True)
    option2 = models.CharField(max_length=1024, null=True)
    option3 = models.CharField(max_length=1024, null=True)
    option4 = models.CharField(max_length=1024, null=True)
    answer = models.CharField(max_length=1024, null=True)

    def __str__(self) -> str:
        return self.question


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