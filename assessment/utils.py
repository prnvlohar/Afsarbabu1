
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import threading


def send_email_with_marks(request, score):
    subject = 'Assessment Marks'
    from_email = settings.EMAIL_HOST_USER
    to = request.user.email
    message = f"This is an <strong>important</strong> message. your total marks is {score}."
    # message.content_subtype = 'html'
    send_mail(subject, message, from_email, [to])


def get_option_alias(option, question):
    if option == question.option1:
        return 'A'
    elif option == question.option2:
        return 'B'
    elif option == question.option3:
        return 'C'
    elif option == question.option4:
        return 'D'
    

def send_mail(subject, plain_text, html_content, to_mail):
    message = EmailMultiAlternatives(
        subject=subject, body=plain_text, to=[to_mail]
    )
    message.attach_alternative(html_content, "text/html")
    message.send()


def send_mail_tread(subject, plain_text, html_content, to_mail):
    t = threading.Thread(
        target=send_mail, args=(
            subject, plain_text, html_content, to_mail
        )
    )
    t.start()
