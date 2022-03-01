from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings

from .celery import app


@app.task
def send_email(subject, user, template, content, from_email=settings.DEFAULT_FROM_EMAIL):
    to = user if isinstance(user, list) else [user]
    # ctx = {'content': content}

    message = get_template(template).render(content)
    msg = EmailMessage(subject, message, from_email=from_email, bcc=to)

    msg.content_subtype = 'html'
    msg.send()
