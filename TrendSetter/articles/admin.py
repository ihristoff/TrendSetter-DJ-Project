from django.contrib import admin

from TrendSetter.articles.models import EducationalArticle, Comment


# Register your models here.
@admin.register(EducationalArticle)
class EducationArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass