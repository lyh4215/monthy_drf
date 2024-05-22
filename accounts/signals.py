from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from blog.models import Post
from datetime import datetime

TUTORIAL_THUMB = 'Have a nice month!'
TUTORIAL_BODY = '''
{"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"간단한 사용법"}]},{"type":"orderedList","attrs":{"start":1},"content":[{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"달력에 넣을 사진에 별표"}]}]},{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"문장은 꾸욱 드래그해서 별표"}]}]},{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"공개한 일기는 링크를 알려준 친구만 볼 수 있어요"}]}]}]},{"type":"paragraph"},{"type":"paragraph"},{"type":"paragraph","content":[{"type":"text","marks":[{"type":"thumb"}],"text":"Have a nice month!"}]},{"type":"paragraph"}]}
'''

@receiver(post_save, sender=User)
def set_username_from_email(sender, instance, created, **kwargs):
    if created and not instance.username:
        instance.username = instance.email
        instance.save()

@receiver(post_save, sender=User)
def set_default_post(sender, instance, created, **kwargs):
    if created:
        Post.objects.create(
            author=instance,
            date=datetime.now().date(),
            published=False,
            thumbType=Post.ThumbnailType.LINE,
            thumbContent=TUTORIAL_THUMB,
            body=TUTORIAL_BODY
        )