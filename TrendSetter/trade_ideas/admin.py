from django.contrib import admin
from django.db import models
from TrendSetter.trade_ideas.models import TradeIdea

# Register your models here.
from django.contrib import admin
from .models import TradeIdea, Comment


@admin.register(TradeIdea)
class TradeIdeaAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'symbol', 'timeframe', 'category', 'created_at', 'updated_at', 'views')
    list_filter = ('symbol', 'timeframe', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'author_name': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'idea', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content',)
