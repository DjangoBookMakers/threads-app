# Generated by Django 5.1.7 on 2025-03-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
