from rest_framework.response import Response
from rest_framework import status
import requests
import os
from .models import User
from .serializers import UserSerializer
from django.shortcuts import redirect

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.kakao import views as kakao_views
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

BASE_URL = os.getenv('BASE_URL')
KAKAO_CALLBACK_URI = os.getenv('SOCIAL_AUTH_KAKAO_CALLBACK_URI')
KAKAO_SOCIAL_LOGIN_URI = BASE_URL + "/accounts/kakao/login/complete/"

KAKAO_AUTHORIZE_API = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_API = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_API = "https://kapi.kakao.com/v2/user/me"
KAKAO_CLIENT_ID = os.getenv('SOCIAL_AUTH_KAKAO_CLIENT_ID')

class KakaoSocialLogin(SocialLoginView): 
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    

class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'address'
    permission_classes = [AllowAny]

    # def get_object(self):
    #     address = self.kwargs.get('address')
    #     return User.objects.get(address=address)