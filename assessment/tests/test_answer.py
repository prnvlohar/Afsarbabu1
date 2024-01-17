from django.test import TestCase
from faker import Factory

from assessment.tests.factory import (AnswerFactory, AssessmentFactory,
                                      QuestionFactory)
from users.tests.factory_user import UserFactory

faker = Factory.create()


