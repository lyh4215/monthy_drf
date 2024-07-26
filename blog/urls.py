import blog.views as views
from django.urls import path

urlpatterns = [
    path(r'posts/me/', views.PostListAPIView.as_view()),
    path(r'posts/user/<str:address>/', views.PostListWithImageLinkAPIView.as_view()),
    path(r'post/', views.PostCreateAPIView.as_view()),
    path(r'post/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path(r'uploadimage/', views.PostImageCreateAPIView.as_view()),
    path(r'discardimage/', views.PostImageDestroyAPIView.as_view()),
    path(r'image/', views.PostImageRetrieveAPIView.as_view()),
]