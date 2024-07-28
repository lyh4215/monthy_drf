# Generated by Django 5.0 on 2024-07-24 03:23

from django.db import migrations
import json

def post_image_fk(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    Post = apps.get_model('blog', 'Post')

    query = Post.objects.all()
    for post in query:
        body = post.body
        body_dict = json.loads(body)
        for page in body_dict['content']:
            if page['type'] == 'image':
                try:
                    url = page['attrs']['src'].replace('https://monthy-image-bucket.s3.amazonaws.com/', '')
                    obj = PostImage.objects.get(src=url)
                    obj.post = post
                    obj.save()
                except:
                    pass
        thumbType = post.thumbType
        if thumbType == 1: #image
            try:
                url = post.thumbContent.replace('https://monthy-image-bucket.s3.amazonaws.com/', '')
                post.thumbContent = url
                post.save()
                obj = PostImage.objects.get(src=url)
                obj.post = post
                obj.save()
            except:
                pass

def reverse_post_image_fk(apps, schema_editor):
    PostImage = apps.get_model('blog', 'PostImage')
    for post_image in PostImage.objects.all():
        post_image.post = None
        post_image.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_postimage_post'),
    ]

    operations = [
        migrations.RunPython(post_image_fk, reverse_post_image_fk),
    ]
