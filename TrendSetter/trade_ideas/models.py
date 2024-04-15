from django.contrib.auth import get_user_model
from django.db import models

from TrendSetter.articles.validators import image_size_validator


UserModel = get_user_model()
class TradeIdea(models.Model):
    MAX_MARKET_LENGTH = 15

    TIMEFRAME_CHOICES = [
        ('15M', '15M'),
        ('30M', '30M'),
        ('1H', '1H'),
        ('4H', '4H'),
        ('1D', '1D'),
        ('1W', '1W'),
        ('1M', '1M'),
    ]

    SYMBOL_CHOICES = [
        ('FX:EURUSD', 'EURUSD'),
        ('FX:GBPUSD', 'GBPUSD'),
        ('FX:USDCHF', 'USDCHF'),
        ('FX:USDJPY', 'USDJPY'),
        ('FX:EURJPY', 'EURJPY'),
        ('FX:AUDUSD', 'AUDUSD'),
        ('COINBASE:BTCUSD', 'BTCUSD'),
        ('COINBASE:ETHUSD', 'ETHUSD'),
        ('AMEX:SPY', 'SPY'),
        ('NASDAQ:NDX', 'NASDAQ'),
        ('NASDAQ:AAPL', 'AAPL'),
        ('NASDAQ:TSLA', 'TSLA'),
        ('NASDAQ:NVDA', 'NVDA'),
        ('NASDAQ:AMZN', 'AMZN'),
        ('SAXO:XAUUSD', 'GOLD'),
        ('SAXO:XAGUSD', 'SILVER'),
        ('Other', 'Other'),
    ]

    CATEGORY_CHOICES = [
        ('Forex', 'Forex'),
        ('Crypto', 'Crypto'),
        ('Indicies', 'Indicies'),
        ('Stocks', 'Stocks'),
        ('Commodites', 'Commodities'),
        ('Other', 'Other'),

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
        choices=SYMBOL_CHOICES,
        null=False,
        blank=False,
    )

    timeframe = models.CharField(max_length=20, choices=TIMEFRAME_CHOICES)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Forex')

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.views += 1
        self.save()

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING,related_name='idea_comments')
    idea = models.ForeignKey(TradeIdea, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}\'s comment- {self.created_at}'