from django.dispatch import receiver
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import transaction
from django.db.models import Q

from user.models import User
from chat.models import Room, Status, Chat

from .serializers import ChatRoomUserlistSerializer, ChatRoomMessagesSerializer
from _utils.query_utils import query_debugger # Query Debugger

from datetime import datetime

# user/?user_id={user_id}
class LoginUserInfoView(APIView):
    @query_debugger
    def get(self, request):
        # request.user
        # login_user_id = request.query_params.get('user_id')
        return Response({"login_username": request.user.username}, status=status.HTTP_200_OK)

        # user_email = 'yubi5050@naver.com' # request.user
# chat/rooms/
class ChatRoomUserlistView(APIView):
    @query_debugger
    def get(self, request):
        user_id = request.query_params.get('user_id')
        # user_email = 'yubi5050@naver.com' # request.user
        
        room = Room.objects.filter(Q(user1=user_id) | Q(user2=user_id))
        room_user_list_serializer_data = ChatRoomUserlistSerializer(room, many=True).data
        # user_info = User.objects.get(id = user_id)
        # user_serializer_data = ChatRoomUserlistSerializer(user_info).data
        print('===', type(room_user_list_serializer_data), room_user_list_serializer_data)
        return Response(room_user_list_serializer_data, status.HTTP_200_OK)

class ChatRoomStatusView(APIView):
    @query_debugger
    @transaction.atomic()
    def post(self, request, roomname):
        # roomname = request.POST.get('roomname')
        user1 = request.POST.get('user1') # requset.user
        user2 = request.POST.get('user2')
        print('===', roomname, user1, user2)
        user1 = User.objects.get(username=user1)
        user2 = User.objects.get(username=user2)
        room_status = Status.objects.get(status='start')
        try:
            room = Room.objects.get(name=roomname)
            Room.objects.filter(id=room.id).update(status=room_status, lasted_time=datetime.now())
        except Room.DoesNotExist:
            room = Room(name = roomname, user1 = user1, user2 = user2, status=room_status,
                        lasted_time=datetime.now(), lasted_message='')
            room.save()
            return Response({"message": "Room does not exist and was Created"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Room is existed and Status Updated"}, status=status.HTTP_200_OK)

class ChatRoomMessagesView(APIView):
    @query_debugger
    def get(self, request, roomname):
        print('===', roomname)
        # room, send_user, receive_user, send_time, message,
        room = Room.objects.get(name=roomname)

        chat_messages_data = ChatRoomMessagesSerializer(room).data
        return Response(chat_messages_data, status=status.HTTP_200_OK)

class SaveChatMessageView(APIView):
    @query_debugger
    @transaction.atomic()
    def post(self, request):
        user1 = request.POST.get('user1') # requset.user
        user2 = request.POST.get('user2')
        roomname = request.POST.get('roomname')
        send_time = request.POST.get('send_time')
        message = request.POST.get('message')
        print('===', roomname, user1, user2, send_time, message)

        user1 = User.objects.get(username=user1)
        user2 = User.objects.get(username=user2)
        room = Room.objects.get(name=roomname)

        date_time_obj = datetime.strptime(send_time, '%Y-%m-%d %H:%M:%S')
        print('=== 시간:', date_time_obj)

        # chat 생성 및 Room의 last_text updated
        chat = Chat(room=room, send_user=user1, receive_user = user2, send_time = send_time, message=message)
        chat.save()

        room = Room.objects.filter(name=roomname).update(lasted_message=message)
        return Response({"message": "Chat was Created"}, status=status.HTTP_201_CREATED)


from django.shortcuts import render

def main(request):
    return render(request, 'chat/main.html', {})

def get_room_info(request):
    return 

def room(request, room_name):
    print('여기오긴함?')
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })