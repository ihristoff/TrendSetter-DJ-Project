from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from TrendSetter.accounts.models import Profile

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, *args, **kwargs):
    #created=False when update, and True on creation
    if not created:
        return

    #maybe not needed
    if Profile.objects.filter(pk=instance.pk).first():
       return

    Profile.objects.create(user=instance)

    # #same as:
    # profile = Profile(user=instance)
    # profile.save()


#TODO send mail
