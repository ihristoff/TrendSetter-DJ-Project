from django.contrib.auth import get_user_model
from django.db import models

from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()


class EducationArticle(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='education_articles')
    title = models.CharField(max_length=255, unique=True,)
    image = models.ImageField(upload_to='education_articles/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    gallery = models.ManyToManyField('Gallery', blank=True)

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

        if not self.slug:  # slugify("My name") -> "My-name"
            self.slug = slugify(f"{self.title}")

        super().save(*args, **kwargs)


class Gallery(models.Model):
    image = models.ImageField(upload_to='education_article_gallery/')