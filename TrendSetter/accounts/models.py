from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model
from TrendSetter.accounts.managers import TrendSetterUserManager
from TrendSetter.articles.validators import image_size_validator


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

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"

#if UserModel is called before custom User creation in code i am getting errors
# django.core.exceptions.ImproperlyConfigured: AUTH_USER_MODEL refers to model 'accounts.TrendSetterUser' that has not been installed

#User Data

#TODO: Profile fields
class Profile(models.Model):
    # DISPLAY_CHOICES = [
    #     ('first_last', 'First Name Last Name'),
    #     ('username', 'Username'),
    #     ('email', 'Email'),
    # ]
    #
    # display_preference = models.CharField(
    #     max_length=20,
    #     choices=DISPLAY_CHOICES,
    #     default='first_last',
    # )

    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
    EXPERT = 'Expert'

    EXPERIENCE_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
        (EXPERT, 'Expert'),
    ]

    user = models.OneToOneField(

        TrendSetterUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_image = models.ImageField(
        upload_to='profile_images/',
        validators=(image_size_validator,),
    )

    username = models.CharField(max_length=25, unique=True, null=True, blank=True)

    send_mail_for_new_article=models.BooleanField(default=False)
    show_email = models.BooleanField(default=True)

    bio = models.CharField(max_length=500, null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    location = models.CharField(max_length=50, null=True, blank=True)

    trading_experience = models.CharField(
        max_length=12,
        choices=EXPERIENCE_CHOICES,
        default=BEGINNER,
    )

    # followers = models.ManyToManyField(User, related_name='following', blank=True)



 # # Add any additional fields related to the user profile
 #    def __str__(self):
 #        return self.user.email
#



    # @property
    # def full_name(self):
    #     if self.first_name and self.last_name:
    #         return f'{self.first_name} {self.last_name}'
    #
    #     return self.first_name or self.last_name