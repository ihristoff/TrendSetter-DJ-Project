# Generated by Django 5.0.3 on 2024-04-16 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_profile_send_mail_for_new_article_profile_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
