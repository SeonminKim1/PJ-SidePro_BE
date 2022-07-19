from django.dispatch import receiver
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import transaction
from user.models import User
from chat.models import Room, Status, Chat

from .serializers import ChatUserSerializer, ChatRoomMessagesSerializer
from _utils.query_utils import query_debugger # Query Debugger

from datetime import datetime

# chat/rooms/
class ChatRoomUserlistView(APIView):
    @query_debugger
    @transaction.atomic()
    def get(self, request):
        user_email = 'yubi5050@naver.com' # request.user
        user_info = User.objects.get(email = user_email)
        print('===', type(user_info), user_info)
        user_serializer_data = ChatUserSerializer(user_info).data
        print('===', type(user_serializer_data), user_serializer_data)

        # products_serializers = ProductsMainSerializer(products, many=True).data
        # print('====', products_serializers)
        # products = Product.objects.all()
        return Response([user_serializer_data], status.HTTP_200_OK)

class ChatRoomStatusView(APIView):
    @query_debugger
    def get(self, request, roomname):
        print('===', roomname)
        # room, send_user, receive_user, send_time, message,
        room = Room.objects.get(name=roomname)

        chat_messages_data = ChatRoomMessagesSerializer(room).data
        return Response(chat_messages_data, status=status.HTTP_200_OK)

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
            Room.objects.filter(id=room.id).update(status=room_status)
        except Room.DoesNotExist:
            room = Room(name = roomname, user1 = user1, user2 = user2, status=room_status,
                        lasted_time=datetime.now(), lasted_message='')
            room.save()
            return Response({"message": "Room does not exist and was Created"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Room is existed and Status Updated"}, status=status.HTTP_200_OK)

# chat/rooms/
class ChatRoomUserlistView(APIView):
    @query_debugger
    @transaction.atomic()
    def get(self, request):
        user_email = 'yubi5050@naver.com' # request.user
        user_info = User.objects.get(email = user_email)
        print('===', type(user_info), user_info)
        user_serializer_data = ChatUserSerializer(user_info).data
        print('===', type(user_serializer_data), user_serializer_data)

        # products_serializers = ProductsMainSerializer(products, many=True).data
        # print('====', products_serializers)
        # products = Product.objects.all()
        return Response([user_serializer_data], status.HTTP_200_OK)

class ChatSendMessageView(APIView):
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