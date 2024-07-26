from accounts.models import User
from django.db.models import UniqueConstraint
from django.db import models
import uuid
import os



class Post(models.Model):
    class ThumbnailType(models.IntegerChoices):
        IMAGE = 1, 'Image'
        HEADING = 2, 'Heading'
        LINE = 3, 'Line'

    thumbType = models.IntegerField(choices=ThumbnailType.choices, default=ThumbnailType.LINE)
    thumbContent = models.CharField(max_length=200, blank=True)
    body = models.TextField()

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['author', 'date'], name='unique_author_date')
        ]

    def __str__(self):
        if self.thumbType == Post.ThumbnailType.IMAGE:
            return f'{self.pk}] {self.author}({self.date}): [Image]'
        elif self.thumbContent != '':
            return f'{self.pk}] {self.author}({self.date}): [Text]'
        else:
            return f'{self.pk}] {self.author}({self.date}): -'

def image_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    return f'images/{instance.post.author.username}/{instance.post.date}/{instance.device_id}/{instance.name_hash}{ext}'

class PostImage(models.Model):
    src = models.ImageField(upload_to=image_upload_to)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    device_id = models.UUIDField()  # UUID4
    name_hash = models.CharField(max_length=100)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['post', 'device_id', 'name_hash'], name='unique_post_device_name_hash')
        ]
    
