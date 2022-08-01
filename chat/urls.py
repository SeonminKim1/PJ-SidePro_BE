# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.ChatRoomUserlistView.as_view(), name='get_roomlist'),
    path('rooms/<str:roomname>/', views.ChatRoomView.as_view(), name='room'),
    path('rooms/<str:roomname>/status/', views.ChatRoomStatusView.as_view(), name='get_roomstatus'),
    path('rooms/<str:roomname>/messages/', views.ChatRoomMessagesView.as_view(), name='get_room_messages'),
    path('messages/', views.SaveChatMessageView.as_view(), name="message")
]