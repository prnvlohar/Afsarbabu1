from django.core.management.base import BaseCommand
from assessment.models import Assessment, Question

class Command(BaseCommand):
    help = 'Assigns question numbers to existing questions per assessment'

    def handle(self, *args, **kwargs):
        assessments = Assessment.objects.all()

        for assessment in assessments:
            questions = Question.objects.filter(assessment=assessment).order_by('id')
            for index, question in enumerate(questions, start=1):
                question.no = index
                question.save()
                self.stdout.write(self.style.SUCCESS(f'Assigned question no {index} for question {question.id} in assessment {assessment.id}'))

        self.stdout.write(self.style.SUCCESS('Successfully assigned question numbers to all assessments'))
