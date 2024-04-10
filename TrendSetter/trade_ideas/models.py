from django.contrib.auth import get_user_model
from django.db import models

from TrendSetter.articles.validators import image_size_validator


UserModel = get_user_model()
class TradeIdea(models.Model):
    MAX_MARKET_LENGTH = 15

    TIMEFRAME_CHOICES = [
        ('short_term', 'Short Term'),
        ('long_term', 'Long Term'),
    ]

    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='trade_ideas')

    title = models.CharField(
        max_length=25,
        null=False,
        blank=False,
    )

    idea_image = models.ImageField(
        upload_to='ideas_images/',
        validators=(image_size_validator,),
        null=False,
        blank=False,
    )

    description = models.TextField()

    symbol = models.CharField(
        max_length=MAX_MARKET_LENGTH,
        null=False,
        blank=False,
    )

    timeframe = models.CharField(max_length=20, choices=TIMEFRAME_CHOICES)

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # views = models.PositiveIntegerField(default=0)

    # def increase_views(self):
    #     self.views += 1
    #     self.save()
