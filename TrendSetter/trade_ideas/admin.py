
from django.contrib import admin
from django.db import models
from TrendSetter.trade_ideas.models import TradeIdea


# Register your models here.
@admin.register(TradeIdea)
class TradeIdeaAdmin(admin.ModelAdmin):
       pass