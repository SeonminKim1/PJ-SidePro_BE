# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('rooms/', views.ChatRoomUserlistView.as_view(), name='get_room_info'),
    path('rooms/<str:roomname>/', views.ChatRoomStatusView.as_view(), name='room'),
    path('message/', views.ChatSendMessageView.as_view(), name="get_chat_message")
    # path('<str:room_name>/', views.room, name='room'),
    # ws://http//127.0.0.1:8000/ws/chat/ABCDE/
]