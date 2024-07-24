import blog.views as views
from django.urls import path

urlpatterns = [
    path(r'posts/<str:address>/', views.PostListAPIView.as_view()),
    path(r'post/', views.PostWithImageCreateAPIView.as_view()),
    path(r'post/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path(r'uploadimage/', views.PostImageCreateAPIView.as_view()),
    path(r'image/', views.PostImageRetrieveDestroyAPIView.as_view()),
]