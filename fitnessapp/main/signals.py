
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.crypto import get_random_string

@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        verification_code=get_random_string(length=50)
        subject='Verify your emial'
        message=f'Your verification code is {verification_code}'
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[instance.email]
        send_mail(subject,message,email_from,recipient_list)


        