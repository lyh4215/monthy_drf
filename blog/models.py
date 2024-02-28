from accounts.models import User
from django.db import models


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
    

    def __str__(self):
        if self.thumbType == Post.ThumbnailType.IMAGE:
            return f'{self.pk}] {self.author}({self.date}): [Image]'
        else:
            return f'{self.pk}] {self.author}({self.date}): {self.thumbContent}'


class PostImage(models.Model):
    src = models.ImageField(upload_to='images/')
