from django.test import TestCase
from django.urls import reverse
from faker import Factory

from assessment.tests.factory import AssessmentFactory, QuestionFactory
from users.tests.factory_user import UserFactory

faker = Factory.create()


class QuestionViewTestCase(TestCase):

    def test_create_assessment(self):
        assessment = AssessmentFactory()
        question = QuestionFactory(assessment=assessment)
        self.assertIsNotNone(question)

    def test_create_question_fail(self):

        test_password = faker.password()
        non_instructor = UserFactory(password=test_password, type='student')
        self.client.login(email=non_instructor.email, password=test_password)

        response = self.client.post(reverse('add-question'), data={})

        self.assertRedirects(response, reverse('index'))