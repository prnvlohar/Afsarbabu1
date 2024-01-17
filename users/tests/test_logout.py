from django.test import TestCase
from django.urls import reverse
from faker import Factory

from users.tests.factory_user import UserFactory

faker = Factory.create()


class LogoutViewTest(TestCase):

    def test_logout(self):

        user_password = faker.password()
        user = UserFactory(password=user_password)

        self.client.login(email=user.email, password=user_password)

        logout_url = reverse('logout')
        response = self.client.get(logout_url)

        self.assertTrue(response)
        self.assertEqual(response.status_code, 302) # 302 is status code for redirect