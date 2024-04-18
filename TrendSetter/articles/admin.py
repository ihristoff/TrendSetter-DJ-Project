from django.contrib import admin

from TrendSetter.articles.models import EducationalArticle, Comment, ArticleRating


# Register your models here.
@admin.register(EducationalArticle)
class EducationalArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at', 'updated_at', 'views')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('title', 'description')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'article', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('content',)


@admin.register(ArticleRating)
class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'rating', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author_name',)
