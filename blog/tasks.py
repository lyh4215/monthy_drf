from monthy_drf.celery import app
from .models import Post, User
from nudge.llm.persona_utils import modify_persona, get_nudge_necessity
from nudge.llm.nudge_utils import make_nudge

@app.task()
def task_modify_persona(post_id):
    post = Post.objects.get(id=post_id)
    modify_persona(post)
    
@app.task()
def task_make_nudge(user_id):
    user = User.objects.get(id=user_id)
    make_nudge(user)