# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('user/', views.LoginUserInfoView.as_view(), name='get_userinfo'),
    path('rooms/', views.ChatRoomUserlistView.as_view(), name='get_roominfo'),
    path('rooms/<str:roomname>/', views.ChatRoomStatusView.as_view(), name='room'),
    path('rooms/<str:roomname>/messages/', views.ChatRoomMessagesView.as_view(), name='get_room'),
    path('messages/', views.SaveChatMessageView.as_view(), name="get_chat_message")
    # path('<str:room_name>/', views.room, name='room'),
    # ws://http//127.0.0.1:8000/ws/chat/ABCDE/
]