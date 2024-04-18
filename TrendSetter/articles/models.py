from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.db import models
from django.db.models import Count
from django.utils.text import slugify

from TrendSetter.articles.validators import image_size_validator
from ckeditor.fields import RichTextField

UserModel = get_user_model()


class EducationalArticle(models.Model):
    CATEGORY_CHOICES = [
        ('Chart patterns', 'Chart patterns'),
        ('Trendlines', 'Trendlines'),
        ('Candlesticks', 'Candlesticks'),
        ('Supply and Demand', 'Supply and Demand'),
        ('Elliott Wave Theory', 'Elliott Wave Theory'),
        ('Volume Analysis', 'Volume Analysis'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='education_articles', null=True,
                             blank=True)
    title = models.CharField(max_length=255, unique=True, )

    # Running on AWS will have problems with uploaded files. It will delete all user created after restart. Use Cloudinary - easy peasy
    image = models.ImageField(
        upload_to='education_articles/',
        validators=(image_size_validator,),
    )

    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, default='Other')
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
        editable=False,  # Readonly, only in the Django App, not in the DB
    )

    author_name = models.CharField(max_length=50, null=True, blank=True)

    def increase_views(self):
        self.views += 1
        self.save()

    def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f"{self.title}")
        if self.user:
            if hasattr(self.user, 'profile') and self.user.profile.username:
                self.author_name = self.user.profile.username
            else:
                email_field_name = UserModel.get_email_field_name()
                self.author_name = getattr(self.user, email_field_name)
            super().save(*args, **kwargs)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}\'s Post- {self.title}'


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, related_name='article_comments', null=True, blank=True)
    article = models.ForeignKey(EducationalArticle, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author_name = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.author:
            if hasattr(self.author, 'profile') and self.author.profile.username:
                self.author_name = self.author.profile.username
            else:
                email_field_name = UserModel.get_email_field_name()
                self.author_name = getattr(self.author, email_field_name)
            super().save(*args, **kwargs)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.author}\'s comment- {self.created_at}'


class ArticleRating(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    article = models.ForeignKey(EducationalArticle, models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    author_name = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.user:
            if hasattr(self.user, 'profile') and self.user.profile.username:
                self.author_name = self.user.profile.username
            else:
                email_field_name = UserModel.get_email_field_name()
                self.author_name = getattr(self.user, email_field_name)
            super().save(*args, **kwargs)

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)
