from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from blog.models import Post
from datetime import datetime

TUTORIAL_THUMB = 'Have a nice month!'
TUTORIAL_BODY = '''
{"type":"doc","content":[{"type":"heading","attrs":{"level":2},"content":[{"type":"text","text":"How to monthy?"}]},{"type":"orderedList","attrs":{"start":1},"content":[{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"클릭해봐요 ->"}]}]},{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"칸마다 "},{"type":"text","marks":[{"type":"bold"}],"text":"썸네일"},{"type":"text","text":"을 지정할 수 있어요!"}]},{"type":"bulletList","content":[{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"문장을 드래그, "},{"type":"text","marks":[{"type":"bold"},{"type":"underline"}],"text":"별표"},{"type":"text","marks":[{"type":"underline"}],"text":" 버튼"}]}]},{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"사진을 클릭, "},{"type":"text","marks":[{"type":"bold"},{"type":"underline"}],"text":"별표"},{"type":"text","marks":[{"type":"underline"}],"text":" 버튼"}]}]}]}]},{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"계절에 어울리는 "},{"type":"text","marks":[{"type":"bold"}],"text":"달력 배너 사진"},{"type":"text","text":"을 설정할 수 있어요. "},{"type":"hardBreak"},{"type":"text","text":"왼쪽 위 톱니바퀴를 눌러봐요!"}]}]},{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"기본적으로 모든 일기는 비공개지만, "}]},{"type":"bulletList","content":[{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":"아래 '눈'을 열어두면 링크를 알려준 친구만 일기를 같이 볼 수 있어요."}]}]}]}]}]},{"type":"paragraph"},{"type":"paragraph","content":[{"type":"text","marks":[{"type":"thumb"}],"text":"Have a monthy month!"}]}]}
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