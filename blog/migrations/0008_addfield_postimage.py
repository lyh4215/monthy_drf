# Generated by Django 5.0 on 2024-07-25 17:28

from django.db import migrations
from django.db import migrations, models
import uuid
import boto3
from django.conf import settings
import os
from django.db.models import Max

def delete_null_post_images(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    PostImage.objects.filter(post__isnull=True).delete()

def reverse_delete_null_post_images(apps, schema_editor):
    # 여기서는 삭제된 데이터를 복구할 수 없으므로 pass
    pass

#set fixed uuid to postImage from anonymous device id
def set_fixed_uuid(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    fixed_uuid = uuid.UUID('123e4567-e89b-12d3-a456-426614174000')
    for post_image in PostImage.objects.all():
        post_image.device_id = fixed_uuid
        post_image.save()

def reverse_fixed_uuid(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    for post_image in PostImage.objects.all():
        post_image.device_id = uuid.uuid4()
        post_image.save()

#initialize index to postImage
def set_index(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    Post = apps.get_model('blog', 'Post')
    for post_image in PostImage.objects.all():
        post: Post = post_image.post
        max_index = PostImage.objects.filter(post=post, device_id=post_image.device_id).aggregate(Max('index'))['index__max'] or 0
        post_image.index = max_index + 1
        post_image.save()

def reverse_set_index(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    for post_image in PostImage.objects.all():
        post_image.index = 0
        post_image.save()

def move_postimages(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    Post = apps.get_model('blog', 'Post')
    #Region NAME?
    S3_URL = "https://monthy-image-bucket.s3.amazonaws.com/"
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    for post_image in PostImage.objects.all():
        old_path = post_image.src.name
        ext = os.path.splitext(old_path)[1]
        new_path = f'images/{post_image.post.author.username}/{post_image.post.date}/{post_image.device_id}/{post_image.index}{ext}'
        s3.copy_object(Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': old_path},
                    Key=new_path)
        s3.delete_object(Bucket=bucket_name, Key=old_path)
        post_image.src.name = new_path
        post_image.save()

        #thumbContent change
        if post_image.post.thumbType == 1:
            if post_image.post.thumbContent == old_path:
                post_image.post.thumbContent = new_path
                post_image.post.save()
        local_new_path = f'images/{post_image.post.date}/{post_image.device_id}/{post_image.index}{ext}'
        
        #body change
        post: Post = post_image.post
        post.body = post.body.replace(S3_URL+old_path, local_new_path)
        post.save()

def reverse_move_postimages(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    Post = apps.get_model('blog', 'Post')
    S3_URL = "https://monthy-image-bucket.s3.amazonaws.com/"
    s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    for post_image in PostImage.objects.all():
        new_path = post_image.src.name
        ext = os.path.splitext(new_path)[1]
        old_path = f'images/{post_image.pk}{ext}'
        s3.copy_object(Bucket=bucket_name,
                    CopySource={'Bucket': bucket_name, 'Key': new_path},
                    Key=old_path)
        s3.delete_object(Bucket=bucket_name, Key=new_path)
        post_image.src.name = old_path
        post_image.save()

        #thumbContent change
        if post_image.post.thumbType == 1:
            if post_image.post.thumbContent == new_path:
                post_image.post.thumbContent = old_path
                post_image.post.save()

        #body change
        post: Post = post_image.post
        local_new_path = f'images/{post_image.post.date}/{post_image.device_id}/{post_image.index}{ext}'
        post.body = post.body.replace(local_new_path, S3_URL+old_path)
        post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_set_postimage_fk'),
    ]

    operations = [
        migrations.RunPython(delete_null_post_images, reverse_delete_null_post_images),
        migrations.AddField(
            model_name='postimage',
            name='device_id',
            field=models.UUIDField(default = uuid.uuid4, editable=False),
        ),
        migrations.RunPython(set_fixed_uuid, reverse_fixed_uuid),
        migrations.AddField(
            model_name='postimage',
            name='index',
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(set_index, reverse_set_index),
        migrations.RunPython(move_postimages, reverse_move_postimages),
    ]