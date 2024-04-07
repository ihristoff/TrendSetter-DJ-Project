from django.contrib import admin

from TrendSetter.articles.models import EducationalArticle


# Register your models here.
@admin.register(EducationalArticle)
class EducationArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')