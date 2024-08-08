from django.urls import path
from nudge import views

urlpatterns = [
    path('', views.NudgeRetrieveAPIView.as_view(), name='nudge'),
    path('confirm/<int:pk>/', views.ConfirmNudgeAPIView.as_view(), name='confirm'),
    path('reject/<int:pk>/', views.RejectNudgeAPIView.as_view(), name='reject'),
]