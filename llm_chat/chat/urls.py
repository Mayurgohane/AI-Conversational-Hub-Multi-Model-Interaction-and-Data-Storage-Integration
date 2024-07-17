from django.urls import path
from .views import ChatAPIView, ChatHistoryAPIView

urlpatterns = [
    path('chat/', ChatAPIView.as_view(), name='chat'),
    path('chat/history/', ChatHistoryAPIView.as_view(), name='chat_history'),
]