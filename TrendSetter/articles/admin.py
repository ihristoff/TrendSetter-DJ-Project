from django.contrib import admin

from TrendSetter.articles.models import EducationalArticle, Comment, ArticleRating


# Register your models here.
@admin.register(EducationalArticle)
class EducationArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(ArticleRating)
class RatingArticleAdmin(admin.ModelAdmin):
    pass

#
#
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['name', 'email', 'article', 'created', 'active']
#     list_filter = ['active', 'created', 'updated']
#     search_fields = ['name', 'email', 'body']