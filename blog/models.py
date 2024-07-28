from accounts.models import User
from django.db.models import UniqueConstraint
from django.db import models
import uuid
import os



class Post(models.Model):
    class ExtraSpanType(models.IntegerChoices):
        DEFAULT = 0, 'Default'
        NARROW = -1, 'Narrow'
        WIDE = 1, 'Wide'

    pages = models.TextField()
    extraSpan = models.IntegerField(choices=ExtraSpanType.choices, default=ExtraSpanType.DEFAULT)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['author', 'date'], name='unique_author_date')
        ]

    def __str__(self):
        return f'{self.pk}] {self.author}({self.date})'

def image_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f'images/{instance.post.author.username}/{instance.post.date}/{instance.device_id}/{instance.name_hash}{ext}'

class PostImage(models.Model):
    src = models.ImageField(upload_to=image_upload_to)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='images')
    device_id = models.UUIDField()  # UUID4
    name_hash = models.CharField(max_length=100)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['post', 'device_id', 'name_hash'], name='unique_post_device_name_hash')
        ]
    
