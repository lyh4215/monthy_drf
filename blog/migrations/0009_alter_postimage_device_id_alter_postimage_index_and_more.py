# Generated by Django 5.0 on 2024-07-25 23:52

import blog.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_addfield_postimage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='device_id',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='index',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='src',
            field=models.ImageField(upload_to=blog.models.image_upload_to),
        ),
        migrations.AddConstraint(
            model_name='post',
            constraint=models.UniqueConstraint(fields=('author', 'date'), name='unique_author_date'),
        ),
        migrations.AddConstraint(
            model_name='postimage',
            constraint=models.UniqueConstraint(fields=('post', 'device_id', 'index'), name='unique_post_device_index'),
        ),
    ]
