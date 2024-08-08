from django.test import TestCase

# Create your tests here.
from nudge.llm.nudge_utils import make_nudge
from nudge.llm.persona_utils import modify_persona
from accounts.models import User


make_nudge(User.objects.get(id=3))