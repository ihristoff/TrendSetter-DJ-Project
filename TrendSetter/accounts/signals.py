from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from TrendSetter.accounts.models import Profile
from TrendSetter.accounts.utils import send_welcome_email

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, *args, **kwargs):

    if not created:
        return

    if Profile.objects.filter(pk=instance.pk).first():
       return

    Profile.objects.create(user=instance)

    send_welcome_email(instance.email)

