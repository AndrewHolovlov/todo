from rest_framework.views import exception_handler

from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if isinstance(response.data, list):
            response.data = {'detail': response.data[0]}

        response.data['status_code'] = response.status_code

    return response


def send_email(subject, user, template, content, from_email=settings.DEFAULT_FROM_EMAIL):
    to = user if isinstance(user, list) else [user]
    # ctx = {'content': content}

    message = get_template(template).render(content)
    msg = EmailMessage(subject, message, from_email=from_email, bcc=to)

    msg.content_subtype = 'html'
    msg.send()
