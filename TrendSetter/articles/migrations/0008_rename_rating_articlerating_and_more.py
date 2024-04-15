# Generated by Django 5.0.3 on 2024-04-14 15:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rating',
            new_name='ArticleRating',
        ),
        migrations.RenameField(
            model_name='articlerating',
            old_name='rate',
            new_name='rating',
        ),
    ]
