from accounts.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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


# class UserKPI(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     class UserType(models.IntegerChoices):
#         NONE_ACTION = 0, 'NoneAction'
#         POST = 1, 'Post'
#         IMAGE = 2, 'Image'

#     userType = models.IntegerField(choices=UserType.choices, default=UserType.NONE_ACTION)

CREATE, READ, UPDATE, DELETE = "Create", "Read", "Update", "Delete"
ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
]

class ActivityLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=15)
    action_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    data = models.JSONField(default=dict)

    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    def __str__(self):
        return f"{self.action_type} by {self.actor} on {self.action_time}"
