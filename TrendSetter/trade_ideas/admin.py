
from django.contrib import admin
from django.db import models
from TrendSetter.trade_ideas.models import TradeIdea


# Register your models here.
@admin.register(TradeIdea)
class TradeIdeaAdmin(admin.ModelAdmin):
       pass

#
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['name', 'email', 'article', 'created', 'active']
#     list_filter = ['active', 'created', 'updated']
#     search_fields = ['name', 'email', 'body']