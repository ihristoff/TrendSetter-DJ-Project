from django.contrib import admin

from TrendSetter.articles.models import EducationArticle


# Register your models here.
@admin.register(EducationArticle)
class EducationArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')