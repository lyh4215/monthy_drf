import social.views as views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r'friends', views.FriendViewSet, basename='friends')
router.register(r'friends/send', views.FriendSendViewSet, basename='friends-send')
router.register(r'friends/receive', views.FriendReceiveViewSet, basename='friends-receive')

urlpatterns = [
    path('', include(router.urls)),

]