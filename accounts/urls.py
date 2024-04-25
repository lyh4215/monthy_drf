import accounts.views as views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path(r'kakao/login/complete/', views.KakaoSocialLogin.as_view(), name='kakao_login_complete'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'logout/', TokenBlacklistView.as_view(), name='logout'),
    path(r'me/', views.UserRetrieveUpdateAPIView.as_view(), name='me'),
    path(r'profile/<str:address>/', views.UserRetrieveAPIView.as_view(), name='profile'),
]