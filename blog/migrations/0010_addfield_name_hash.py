# Generated by Django 5.0 on 2024-07-26 18:30

from django.db import migrations, models
import secrets
import boto3
from django.conf import settings
import os

def generate_random_hash():
    return secrets.token_hex(16)
def set_default_hash(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    for post_image in PostImage.objects.all():
        post_image.name_hash = generate_random_hash()
        post_image.save()
def move_postimages_with_hash(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    Post = apps.get_model('blog', 'Post')
    #Region NAME?
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    for post_image in PostImage.objects.all():
        old_path = post_image.src.name
        ext = os.path.splitext(old_path)[1]
        new_path = f'images/{post_image.post.author.username}/{post_image.post.date}/{post_image.device_id}/{post_image.name_hash}{ext}'
        s3.copy_object(Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': old_path},
                    Key=new_path)
        s3.delete_object(Bucket=bucket_name, Key=old_path)
        post_image.src.name = new_path
        post_image.save()
        #thumbContent change
        local_old_path = f'images/{post_image.post.date}/{post_image.device_id}/{post_image.index}{ext}'
        local_new_path = f'images/{post_image.post.date}/{post_image.device_id}/{post_image.name_hash}{ext}'
        if post_image.post.thumbType == 1:
            if post_image.post.thumbContent == local_old_path:
                post_image.post.thumbContent = local_new_path
                post_image.post.save()
        #body change
        post: Post = post_image.post
        post.body = post.body.replace(local_old_path, local_new_path)
        post.save()

def reverse_move_postimages_with_hash(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    Post = apps.get_model('blog', 'Post')
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    for post_image in PostImage.objects.all():
        new_path = post_image.src.name
        ext = os.path.splitext(new_path)[1]
        old_path = f'images/{post_image.post.author.username}/{post_image.post.date}/{post_image.device_id}/{post_image.index}{ext}'
        
        s3.copy_object(Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': new_path},
                    Key=old_path)
        s3.delete_object(Bucket=bucket_name, Key=new_path)
        post_image.src.name = old_path
        post_image.save()
        #thumbContent change
        local_old_path = f'images/{post_image.post.date}/{post_image.device_id}/{post_image.name_hash}{ext}'
        local_new_path = f'images/{post_image.post.date}/{post_image.device_id}/{post_image.index}{ext}'
        if post_image.post.thumbType == 1:
            if post_image.post.thumbContent == local_new_path:
                post_image.post.thumbContent = local_old_path
                post_image.post.save()
        #body change
        post: Post = post_image.post
        
        post.body = post.body.replace(local_new_path, local_old_path)
        post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_postimage_device_id_alter_postimage_index_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postimage',
            name='name_hash',
            field=models.CharField(max_length=100, default=generate_random_hash()),
        ),
        migrations.RunPython(set_default_hash, migrations.RunPython.noop),
        migrations.RunPython(move_postimages_with_hash, reverse_move_postimages_with_hash)
    ]
