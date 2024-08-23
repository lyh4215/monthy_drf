from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils.text import slugify
import random
import string
from accounts.models import User

class SetUsernameAddressSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        if not user.username:
            email = data.get('email')
            if email:
                base_username = email.split('@')[0]
                user.username = self.generate_unique_username(base_username)
        
        return user

    def generate_unique_username(self, base_username):
        username = slugify(base_username)
        #같은 username 있는 경우 뒷부분에 랜덤str 추가
        while User.objects.filter(username=username).exists():
            username = f"{slugify(base_username)}{self.get_random_string()}"
        return username

    def get_random_string(self, length=4):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))