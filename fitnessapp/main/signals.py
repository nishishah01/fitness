# signals.py
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import UserProfile
from django.utils.crypto import get_random_string

@receiver(post_save, sender=UserProfile)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        verification_code = get_random_string(length=50)
        subject = 'Verify your email'
        message = f'Your verification code is {verification_code}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]

        try:
            send_mail(subject, message, email_from, recipient_list)
            print(f'Email sent to {instance.email}')
        except Exception as e:
            print(f'Error sending email: {e}')
