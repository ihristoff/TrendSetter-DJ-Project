from django.contrib.auth import get_user_model
from django.db import models

from django.db import models
from django.utils.text import slugify

from TrendSetter.articles.validators import image_size_validator
from ckeditor.fields import RichTextField

UserModel = get_user_model()


class EducationalArticle(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='education_articles')
    title = models.CharField(max_length=255, unique=True,)
    image = models.ImageField(
        upload_to='education_articles/',
        validators=(image_size_validator,),
    )
    # category = models.CharField(max_length=25, )
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # gallery = models.ManyToManyField('Gallery', blank=True)

    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
        editable=False,  # Readonly, only in the Django App, not in the DB
    )

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f"{self.title}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}\'s Post- {self.title}'


# class Gallery(models.Model):
#     image = models.ImageField(upload_to='education_article_gallery/')


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    article= models.ForeignKey(EducationalArticle, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}\'s comment- {self.created_at}'
