from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

from TrendSetter.articles.models import EducationalArticle


# Create your models here.
UserModel = get_user_model()


class CommentRating(models.Model):
    article = models.ForeignKey(EducationalArticle, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    comment = models.TextField(max_length=500,
                               blank=True,
                               null=True,
                               )
    rating = models.FloatField()
    # ip_address= models.CharField(max_length=20, blank = True, null = True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user

    # def __str__(self):
    #     return '%s - %s' % (self.article, self.user)
