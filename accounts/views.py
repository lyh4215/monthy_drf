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
from rest_framework_simplejwt.views import TokenRefreshView



BASE_URL = "http://localhost:8000"
KAKAO_CALLBACK_URI = "http://localhost:3000/logincallback/kakao"
KAKAO_SOCIAL_LOGIN_URI = BASE_URL + "/accounts/kakao/login/complete/"

KAKAO_AUTHORIZE_API = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_API = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_API = "https://kapi.kakao.com/v2/user/me"


def kakao_login(request):
    client_id = os.environ.get('SOCIAL_AUTH_KAKAO_CLIENT_ID')
    return redirect(f"{KAKAO_AUTHORIZE_API}?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code")

@api_view(['GET'])
@permission_classes([AllowAny])
def kakao_login_callback(request):
    code = request.GET.get("code")
    if request.GET.get("error") is not None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    token_response = request_token(code)
    if token_response.get('error') is not None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    access_token = token_response.get('access_token')

    user_info_response = request_user_info(access_token)
    if user_info_response.get('error') is not None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # kakao_account = user_info_response.get('kakao_account')
    # email = kakao_account.get('email')

    data = { 'access_token': access_token, 'code': code }
    accept = requests.post(KAKAO_SOCIAL_LOGIN_URI, data=data)
    accpet_status = accept.status_code

    if accpet_status != 200:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    accept_json = accept.json()
    accept_json.pop('user')
    response = Response({ 'access': accept_json.pop('access') }, status=status.HTTP_200_OK)
    response.set_cookie('refresh', accept_json.pop('refresh'), httponly=True)
    return response

def request_token(code):
    headers = {
      "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
      "grant_type": "authorization_code",
      "client_id": os.environ.get('SOCIAL_AUTH_KAKAO_CLIENT_ID'),
      "redirect_uri": KAKAO_CALLBACK_URI,
      "code": code
    }

    token_response = requests.post(KAKAO_TOKEN_API, data=data, headers=headers).json()
    return token_response

def request_user_info(access_token):
    headers = {
      # "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": f"Bearer ${access_token}"
    }
    user_info_response = requests.get(KAKAO_USER_API, headers=headers).json()
    return user_info_response       


class KakaoSocialLogin(SocialLoginView): 
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh')
        if refresh is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.data['refresh'] = refresh
        return super().post(request, *args, **kwargs) 
           

class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user