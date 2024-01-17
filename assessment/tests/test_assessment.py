from django.test import TestCase
from faker import Factory

from assessment.tests.factory import AssessmentFactory
from courses.tests.factory import CourseFactory, LectureFactory

faker = Factory.create()


class AssessmentViewTestCase(TestCase):

    def test_create_assessment(self):
        course = CourseFactory()
        assessment = AssessmentFactory(course=course)
        self.assertIsNotNone(assessment)