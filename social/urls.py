import social.views as views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'friend/send', views.FriendSendViewSet, basename='friends-send')
router.register(r'friend/receive', views.FriendReceiveViewSet, basename='friends-receive')
router.register(r'blocked', views.BlockedUserViewSet, basename='blocked')

urlpatterns = [
    path('', include(router.urls)),

]