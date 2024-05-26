from celery import shared_task
from django.contrib.auth.views import get_user_model
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

import logging

log = logging.getLogger('celery')
User = get_user_model()


@shared_task(queue='high_priority')
def send_message_to_confirm_email(domain, user_id, token):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logging.error(f"User with id: {user_id} does not exist. Email not sent.")
        return f"Message wasn't sent because user with id: {user_id} does not exist."

    template = 'accounts/auth/confirm_email_template.html'
    subject = "Email Confirmation"
    receiver_email = user.email
    context = {'user': user,
               'domain': domain,
               'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
               'token': token,
               'life_time': str(settings.PASSWORD_RESET_TIMEOUT // 60)}

    body = render_to_string(template, context)
    mail = EmailMultiAlternatives(subject=subject, to=[receiver_email])
    mail.attach_alternative(body, "text/html")

    try:
        mail.send()
        logging.info(f"Email sent to {receiver_email}")
        return f"Message was sent to {receiver_email}"
    except Exception as e:
        logging.error(f"Failed to send email to {receiver_email}: {e}")
        return f"Failed to send message to {receiver_email}"
