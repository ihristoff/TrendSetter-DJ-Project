from django.contrib import admin

from TrendSetter.ratings.models import CommentRating

#
# # Register your models here.
@admin.register(CommentRating)
class CommentRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'comment', 'created_at','status')

