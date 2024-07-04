

import secrets
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import string
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
from django.views import View

from assessment.models import Assessment
from users.forms import LoginForm, RegisterForm, UsersForm
from users.models import CustomUser
from users.tokens import email_verification_token, generate_referral_code

User = settings.AUTH_USER_MODEL


class RegisterView(View):
    form_class = RegisterForm
    template_name = "users/registration.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/index?login=True")
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.is_active = False

            referral_code = request.POST.get('token')
            if referral_code:
                reccommended_user = CustomUser.objects.get(
                    referral_code=referral_code
                )
                user.recommended_by = reccommended_user

            user.save()

            current_site = get_current_site(request)
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
                subject=subject, body=plain_text, to=[user.email]
            )
            message.attach_alternative(html_content, "text/html")
            message.send()

            messages.success(request, 'Please verify your email.')
            return redirect("login")
        else:
            messages.error(request, form.errors)
            return redirect("register")

class InstituteRegisterView(View):

    """ Institute registration with mail confirmation """

    form_class = RegisterForm
    template_name = "users/institute_reg.html"


    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/index?login=True")
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.type = 'institute'
            user.password = make_password(user.password)
            user.is_active = False
            user.referral_code = generate_referral_code()
            user.institute = form.cleaned_data['institute']

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
            return redirect("/institute_reg/")


class LoginView(View):

    """ Login here via email and password """

    form_class = LoginForm
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('index')+"?login=True")
        login_form = self.form_class()
        return render(request, self.template_name, {"login_form": login_form})

    def post(self, request, *args, **kwargs):

        login_form = self.form_class()
        payload = request.POST
        email = payload.get('email', '')
        user_password = payload.get('password', '')
        user = authenticate(email=email, password=user_password)
        if user is None:
            messages.success(
                request, 'Please verify email or check email / password')
            return redirect('login')
        else:
            login(request, user)
            return redirect(reverse('index'))


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
        elif user.type == 'instructor' or user.type == 'institute':
            user.is_active = True
            user.is_staff = True
            user.save()
        return HttpResponseRedirect(reverse('login'))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def generate_random_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


def create_users(num_users, institute):
    users = []
    temp_password = [generate_random_password(10) for i in range(num_users)]
    for i in range(num_users):
        email = f"{institute}{i}_{secrets.token_hex(4)}@afsarbabu.in"
        while CustomUser.objects.filter(email=email).exists():
            email = f"{institute}{i}_{secrets.token_hex(4)}@afsarbabu.in"
        user = CustomUser(email=email, type='student')
        user.set_password(temp_password[i])
        users.append(user)
    CustomUser.objects.bulk_create(users)

    df = pd.DataFrame([{'email': user.email, 'password': temp_password[i]}
                       for i, user in enumerate(users)])
    return df


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
            df = create_users(num_users, institute)
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{institute}_students_credentials.xlsx"'
            df.to_excel(response, index=False)
            return response
        else:
            messages.error(request, 'Users creation failed.')
            return HttpResponseRedirect(reverse('users'))


class LinkView(View):
    def get(self, request):
        users = CustomUser.objects.exclude(referral_code='').filter(referral_code__isnull=False)
        signup_url = reverse('register')
        return render(request, 'users/link.html', {'signup_url': signup_url, 'users': users})



from django.shortcuts import render
from .razorpay import *

def payment_view(request):
   amount = 100  # Set the amount dynamically or based on your requirements
   order_id = initiate_payment(amount)
   context = {
       'order_id': order_id,
       'amount': amount
   }
   return render(request, 'users/payment.html', context)


def payment_success_view(request):
   order_id = request.POST.get('order_id')
   payment_id = request.POST.get('razorpay_payment_id')
   signature = request.POST.get('razorpay_signature')
   params_dict = {
       'razorpay_order_id': order_id,
       'razorpay_payment_id': payment_id,
       'razorpay_signature': signature
   }
   try:
       client.utility.verify_payment_signature(params_dict)
       # Payment signature verification successful
       # Perform any required actions (e.g., update the order status)
       return HttpResponse("success")
   except razorpay.errors.SignatureVerificationError as e:
       # Payment signature verification failed
       # Handle the error accordingly
       return HttpResponse("fail")
