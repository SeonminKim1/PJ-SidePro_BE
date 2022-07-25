# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.ChatRoomUserlistView.as_view(), name='get_roominfo'),
    path('rooms/<str:roomname>/', views.ChatRoomView.as_view(), name='room'),
    path('rooms/<str:roomname>/status/', views.ChatRoomStatusView.as_view(), name='room'),
    path('rooms/<str:roomname>/messages/', views.ChatRoomMessagesView.as_view(), name='get_room'),
    path('messages/', views.SaveChatMessageView.as_view(), name="get_chat_message")
]