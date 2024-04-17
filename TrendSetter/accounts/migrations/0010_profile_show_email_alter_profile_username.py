# Generated by Django 5.0.3 on 2024-04-16 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='show_email',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True),
        ),
    ]
