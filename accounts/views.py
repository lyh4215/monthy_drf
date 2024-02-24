from rest_framework.response import Response
from rest_framework import status
import requests
import os
from .models import User
from django.http import JsonResponse
from django.shortcuts import redirect

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.kakao import views as kakao_views

BASE_URL = "http://localhost:8000"
KAKAO_AUTHORIZE_API = "https://kauth.kakao.com/oauth/authorize"
KAKAO_TOKEN_API = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_API = "https://kapi.kakao.com/v2/user/me"
KAKAO_CALLBACK_URI = "http://localhost:8000/accounts/kakao/login/callback"
KAKAO_SOCIAL_LOGIN_URI = "http://localhost:8000/accounts/kakao/login/complete/"


def kakao_login(request):
    client_id = os.environ.get('SOCIAL_AUTH_KAKAO_CLIENT_ID')
    return redirect(f"{KAKAO_AUTHORIZE_API}?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code")

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
    return JsonResponse(accept_json)

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
        