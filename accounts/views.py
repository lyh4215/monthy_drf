from rest_framework.response import Response
from rest_framework import status
import requests
import os
from .models import User
from .serializers import UserSerializer, TokenValidationSerializer
from django.shortcuts import redirect

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.apple import views as apple_views
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

BASE_URL = os.getenv('BASE_URL')
KAKAO_CALLBACK_URI = os.getenv('SOCIAL_AUTH_KAKAO_CALLBACK_URI')
KAKAO_SOCIAL_LOGIN_URI = BASE_URL + "/accounts/kakao/login/complete/"

APPLE_CALLBACK_URI = os.getenv('SOCIAL_AUTH_APPLE_CALLBACK_URI')
APPLE_SOCIAL_LOGIN_URI = BASE_URL + "/accounts/apple/login/complete/"

KAKAO_AUTHORIZE_API = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_API = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_API = "https://kapi.kakao.com/v2/user/me"
KAKAO_CLIENT_ID = os.getenv('SOCIAL_AUTH_KAKAO_CLIENT_ID')

class KakaoSocialLogin(SocialLoginView): 
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI

class AppleSocialLogin(SocialLoginView): 
    adapter_class = apple_views.AppleOAuth2Adapter
    client_class = OAuth2Client
    #callback_url = APPLE_CALLBACK_URI

class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        response_data = serializer.data.copy()
        response_data['provider'] = self.get_provider(user)
        return Response(response_data)
    
    def get_provider(self, user):
        providers = []
        for social_account in user.socialaccount_set.all():
            providers.append(social_account.provider)
        return providers

class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'address'
    permission_classes = [AllowAny]

    # def get_object(self):
    #     address = self.kwargs.get('address')
    #     return User.objects.get(address=address)

class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
class AppleUserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = TokenValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['refresh_token']

        payload = {
            'client_id': os.getenv('SOCIAL_AUTH_APPLE_CLIENT_ID'),
            'client_secret': os.getenv('SOCIAL_AUTH_APPLE_CLIENT_SECRET'),
            'token': token,
            'token_type_hint': 'refresh_token'
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post('https://appleid.apple.com/auth/revoke', data=payload, headers=headers)
        if response.status_code == 200:
            self.perform_destroy(user)
            return Response({'message': 'user deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'message': 'apple token revoke failed'}, status=status.HTTP_400_BAD_REQUEST)