import accounts.views as views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path(r'kakao/login/', views.kakao_login, name='kakao_login'),
    path(r'kakao/login/code/', views.kakao_login_callback, name='kakao_login_callback'),
    path(r'kakao/login/complete/', views.KakaoSocialLogin.as_view(), name='kakao_login_complete'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'me/', views.UserRetrieveUpdateAPIView.as_view(), name='me'),
]