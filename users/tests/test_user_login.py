from django.test import Client, SimpleTestCase, TestCase
from django.urls import resolve, reverse
# from django.contrib.auth import get_user_model
from faker import Factory

from users.forms import LoginForm
from users.models import CustomUser
from users.tests.factory_user import UserFactory

faker = Factory.create()

# # Create your tests here.


class LoginViewTest(TestCase):

    def setUp(self):

        self.test_password = faker.password()
        self.user = UserFactory(password=self.test_password)

    def test_login_success(self):

        # logged_in = self.client.login(
        #     email=self.user.email, password=self.test_password)

        # self.assertTrue(logged_in)
        login_url = reverse('login')
        data = {
            'email': self.user.email,
            'password': self.test_password,
        }
        response = self.client.post(login_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_login_fail_email_and_password_field_is_blank(self):

        data = {
            'email': '',
            'password': ''
        }

        form = LoginForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue(form['email'].errors, [
                        'Enter a valid email'])
        self.assertTrue(form['password'].errors, [
            'Enter a valid password.'])

    def test_login_fail_email_field_is_blank(self):

        data = {
            'email': '',
            'password': faker.password()
        }

        form = LoginForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue(form['email'].errors, [
                        'Enter a valid email'])

    def test_login_fail_password_field_is_blank(self):

        data = {
            'email': faker.email(),
            'password': ''
        }

        form = LoginForm(data)

        self.assertFalse(form.is_valid())
        self.assertTrue(form['password'].errors, [
            'Enter a valid password.'])

    def test_login_fail_email_is_not_register(self):

        log_in = self.client.login(
            email=faker.email(), password=self.test_password)

        self.assertFalse(log_in)

    def test_login_fail_password_is_not_match(self):

        log_in = self.client.login(
            email=self.user.email, password=faker.password())

        self.assertFalse(log_in)
