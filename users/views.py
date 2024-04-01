

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import (HttpResponse, HttpResponseRedirect, redirect,
                              render)
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from enrollment.forms import EnrollForm
from django.views import View

from assessment.models import Assessment
from users.forms import LoginForm, RegisterForm, UsersForm
from users.models import CustomUser
from users.tokens import email_verification_token

User = settings.AUTH_USER_MODEL



class RegisterView(View):

    """ User registration with mail confirmation """

    form_class = RegisterForm
    template_name = "users/registration.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/index?login=True")
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = 'student'
            user.password = make_password(user.password)
            user.is_active = False

            user.save()
            current_site = get_current_site(self.request)
            subject = 'Activate Your Account'
            html_content = render_to_string(
                'users/email_verification.html',
                {
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': email_verification_token.make_token(user),
                }
            )
            plain_text = strip_tags(html_content)
            message = EmailMultiAlternatives(
                to=[user.email], subject=subject, body=plain_text)
            message.content_subtype = "html"
            message.attach_alternative(html_content, "text/html")
            message.send()
            messages.success(request, 'verify your email.')
            return redirect("login")
        else:
            err = form.errors
            messages.error(
                request, err)
            return redirect("/register/")


class LoginView(View):

    """ Login here via email and password """

    form_class = LoginForm
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/index?login=True")
        login_form = self.form_class()
        return render(request, self.template_name, {"login_form": login_form})

    def post(self, request, *args, **kwargs):

        login_form = self.form_class()
        payload = request.POST
        email = payload.get('email', '')
        user_password = payload.get('password', '')
        user = authenticate(email=email, password=user_password)
        if user is None:
            # print()
            messages.success(
                request, 'Please verify email or check email / password')
            return redirect('login')
        else:
            login(request, user)
            return redirect('/index/')


@login_required
def index_view(request):
    assessments = Assessment.objects.all()
    users = CustomUser.objects.all()
    return render(request, 'users/index.html', {
                                                'users': users,
                                                'assessments': assessments,
                                                })


class ActivateView(View):

    """ User's email verification """

    def get_user_from_email_verification(self, uid, token: str):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                get_user_model().DoesNotExist):
            return None

        if user is not None \
                and \
                email_verification_token.check_token(user, token):
            return user
        else:
            return None

    def get(self, request, uidb64, token):
        user = self.get_user_from_email_verification(uidb64, token)
        if user.type == 'student':
            user.is_active = True
            user.save()
        elif user.type == 'instructor':
            user.is_active = True
            user.is_staff = True
            user.save()
        return HttpResponseRedirect(reverse('login'))

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

import secrets
import string
import pandas as pd
from django.http import HttpResponse
import os

def generate_random_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

def create_users(request, num_users, institute):
    users = []
    temp_password = []
    for i in range(num_users):
        email = f"{institute}{i}_{secrets.token_hex(4)}@afsarbabu.in"
        while CustomUser.objects.filter(email=email).exists():
            email = f"{institute}{i}_{secrets.token_hex(4)}@afsarbabu.in"
        password = generate_random_password(10)
        temp_password.append(password)
        user = CustomUser(email=email, type='student')
        user.set_password(password)
        users.append(user)
    CustomUser.objects.bulk_create(users)

    df = pd.DataFrame([{'email': user.email, 'password': temp_password[i]}
            for i, user in enumerate(users)])
    filename = "users.xlsx"
    df.to_excel(filename, index=False)
    # download xlsx file in browser
    return filename



class UsersView(View):

    form_class = UsersForm
    template_name = "users/users.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            institute = form.cleaned_data['institute']
            num_users = int(form.cleaned_data['students'])
            filename = create_users(request, num_users, institute)
            with open(f'/home/developer/Desktop/Django/Afsarbabu1/Afsarbabu1/{filename}', 'rb') as fh:
                response = HttpResponse(fh.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{institute}_students_credentials.xlsx"'
                os.remove(filename)
                return response
        else:
            messages.error(request, 'Users creation failed.')
            return HttpResponseRedirect(reverse('users'))
