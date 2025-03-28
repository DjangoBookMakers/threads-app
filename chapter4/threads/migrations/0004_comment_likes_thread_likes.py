# Generated by Django 5.1.7 on 2025-03-28 08:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0003_alter_thread_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='thread',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_threads', to=settings.AUTH_USER_MODEL),
        ),
    ]
