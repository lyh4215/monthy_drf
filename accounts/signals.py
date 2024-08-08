from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from blog.models import Post
from datetime import datetime

TUTORIAL_THUMB = '마음에 드는 문장'
TUTORIAL_BODY = '''
{"type":"doc","content":[{"type":"heading","attrs":{"level":2},"content":[{"type":"text","text":"How to monthy?"}]},{"type":"paragraph","content":[{"type":"text","text":"클릭해서 바로 수정할 수 있어요. "}]},{"type":"paragraph","content":[{"type":"text","text":"monthy의 핵심은 "},{"type":"text","marks":[{"type":"bold"}],"text":"별표"},{"type":"text","text":" 버튼! ⭐️ (수정할 때만 보여요)"}]},{"type":"paragraph","content":[{"type":"text","text":"이렇게 "},{"type":"text","marks":[{"type":"thumb"}],"text":"마음에 드는 문장"},{"type":"text","text":"을 "},{"type":"text","marks":[{"type":"bold"}],"text":"드래그"},{"type":"text","text":"해서 "},{"type":"text","marks":[{"type":"underline"}],"text":"제목"},{"type":"text","text":"을 지정할 수도 있구요, 오늘의 "},{"type":"text","marks":[{"type":"underline"}],"text":"대표 사진"},{"type":"text","text":"을 설정할 수도 있어요!"}]},{"type":"paragraph"},{"type":"paragraph"},{"type":"paragraph"},{"type":"paragraph","content":[{"type":"text","text":"     추신. 달력 위 배너 사진을 넣을 수 있어요."}]}]}
'''

# @receiver(post_save, sender=User)
# def set_username_from_email(sender, instance, created, **kwargs):
#     if created and not instance.username:
#         instance.username = instance.email
#         instance.save()

# @receiver(post_save, sender=User)
# def set_default_post(sender, instance, created, **kwargs):
#     if created:
#         Post.objects.create(
#             author=instance,
#             date=datetime.now().date(),
#             published=False,
#             body=TUTORIAL_BODY
#         )