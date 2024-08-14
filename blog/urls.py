import blog.views as views
from django.urls import path

urlpatterns = [
    path(r'posts/me/', views.PostListAPIView.as_view()),
    path(r'posts/user/<str:address>/', views.PostListWithImageLinkAPIView.as_view()),
    path(r'post/', views.PostCreateAPIView.as_view()),
    path(r'post/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path(r'uploadimage/<str:date>/<str:device_id>/<str:name_hash>/', views.PostImageCreateAPIView.as_view()),
    path(r'lastupdated/', views.PostUpdatedAtListAPIView.as_view()),
]