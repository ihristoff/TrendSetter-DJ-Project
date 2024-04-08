from django.db import models

from TrendSetter.articles.validators import image_size_validator

class TradeIdea(models.Model):
    MAX_MARKET_LENGTH = 15

    TIMEFRAME_CHOICES = [
        ('short_term', 'Short Term'),
        ('long_term', 'Long Term'),
    ]

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

