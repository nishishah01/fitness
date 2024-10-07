from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens import account_activation_token

from .models import userProfiles



@receiver(post_save, sender=userProfiles)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        user = instance
        if not user.is_active:  # if user is not active send activation email
            uid = user.pk
            token = account_activation_token.make_token(user)

            mail_subject = 'Activate your Fit Genius account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'uid': uid,
                'token': token,
            })

            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            print(f"Activation email sent to {to_email}")
