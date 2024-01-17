
from django.conf import settings
from django.core.mail import send_mail


def send_email_with_marks(request, score):
    subject = 'Assessment Marks'
    from_email = settings.EMAIL_HOST_USER
    to = request.user.email
    message = f"This is an <strong>important</strong> message. your total marks is {score}."
    # message.content_subtype = 'html'
    send_mail(subject, message, from_email, [to])
