from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

# Create your views here.

def home(request):
    return render(request, 'portal/index.html')

def about(request):
    return render(request, 'portal/about.html')
import threading
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

        def send_mail(subject, plain_text, html_content):
            message = EmailMultiAlternatives(
                subject=subject, body=plain_text, to=["afsarbabu010124@gmail.com"]
            )
            message.attach_alternative(html_content, "text/html")
            message.send()

        t = threading.Thread(target=send_mail,
                             args=(subject, plain_text, html_content))
        t.start()
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
