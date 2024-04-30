
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from .models import *
from django_rest_passwordreset.signals import reset_password_token_created
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


User = get_user_model()




@receiver(post_save, sender=User)
def customer_Profile(sender, instance, created, *args, **kwargs):
    if created:
        group = Group.objects.get(name='Customer')
        instance.groups.add(group)

        UserProfile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
        )
        print('User Profile created for', instance.first_name)

@receiver(post_save, sender=User)
def update_Profile(sender, instance, created, *args, **kwargs):
    if not created:
        try:
            instance.userprofile.save()
            print('Profile updated!!!')
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)
            print('User Profile created for existing')




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'first_name': reset_password_token.user.first_name,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Reset Password For Account"),
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()