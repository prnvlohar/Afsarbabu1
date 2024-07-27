from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import threading
from django.utils.html import strip_tags
from assessment.utils import send_mail_tread
from django.conf import settings

# Create your views here.

def home(request):
    return render(request, 'portal/index.html')

def about(request):
    return render(request, 'portal/about.html')
def contact(request):
    if request.method == "GET":
        return render(request, 'portal/contact.html')
    if request.method == "POST":
        payload = request.POST
        name = payload['name']
        email = payload['email']
        phone = payload['phone']
        message = payload['message']
        subject = 'Customer enquiry from - ' + name
        html_content = render_to_string(
            'portal/contact_us_email.html',{
                "name":name,
                "email":email,
                "phone":phone,
                "message":message
            }
        )
        plain_text = strip_tags(html_content)

        send_mail_tread(subject, plain_text, html_content, settings.EMAIL_HOST_USER)

        return render(request, 'portal/contact.html', {"flag":"Enquiry submitted successfully"})

def pricing(request):
    return render(request, 'portal/pricing.html')


def blogHome(request):
    return render(request, 'portal/blog-home.html')

def blogPost1(request):
    return render(request, 'portal/blog-post1.html')
def blogPost2(request):
    return render(request, 'portal/blog-post2.html')
def blogPost3(request):
    return render(request, 'portal/blog-post3.html')
