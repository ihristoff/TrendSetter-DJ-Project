from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from TrendSetter.accounts.managers import TrendSetterUserManager

#Auth Data
class TrendSetterUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    EMAIL_MAX_LENGTH = 50

    email = models.EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        null=False,
        blank=False,
        error_messages={'unique': 'A user with that email already exists',}
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = "email"

    objects= TrendSetterUserManager()

    # def __str__(self):
    #     return self.email

    class Meta:
        verbose_name = "User"

#if UserModel is called before custom User creation in code i am getting errors
# django.core.exceptions.ImproperlyConfigured: AUTH_USER_MODEL refers to model 'accounts.TrendSetterUser' that has not been installed

#User Data

#TODO: Profile fields
class Profile(models.Model):
    user = models.OneToOneField(
        #no need to use UserModel here because both models are in one file
        TrendSetterUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_of_birth = models.DateTimeField(null=True, blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    profile_image = models.URLField(null=True, blank=True)
    trading_from = models.CharField(max_length=50, null=True, blank=True)
 # # Add any additional fields related to the user profile
 #    def __str__(self):
 #        return self.user.email


    # @property
    # def full_name(self):
    #     if self.first_name and self.last_name:
    #         return f'{self.first_name} {self.last_name}'
    #
    #     return self.first_name or self.last_name