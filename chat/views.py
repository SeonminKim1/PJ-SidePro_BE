from django.dispatch import receiver
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.db import transaction
from django.db.models import Q

from user.models import User
from chat.models import Room, Status, Chat
from chat import constants

from .serializers import ChatRoomUserlistSerializer, ChatRoomMessagesSerializer
from _utils.query_utils import query_debugger # Query Debugger
from datetime import datetime
import uuid

# chat/user/?user_id=4
class LoginUserInfoView(APIView):
    @query_debugger
    def get(self, request):
        # request.user
        # login_user_id = request.query_params.get('user_id')
        return Response({"login_username": request.user.username}, status=status.HTTP_200_OK)

# chat/rooms/?user_id=4
class ChatRoomUserlistView(APIView):
    @query_debugger
    def get(self, request):
        user_id = request.query_params.get('user_id')
        
        room = Room.objects.filter(Q(user1=user_id) | Q(user2=user_id))
        room_user_list_serializer_data = ChatRoomUserlistSerializer(room, many=True).data
        # user_info = User.objects.get(id = user_id)
        # user_serializer_data = ChatRoomUserlistSerializer(user_info).data
        # print('===', type(room_user_list_serializer_data), room_user_list_serializer_data)
        return Response(room_user_list_serializer_data, status.HTTP_200_OK)

# chat/rooms/<str:roomname>/
# ROOM 생성 / 삭제 관련
class ChatRoomView(APIView):
    @query_debugger
    @transaction.atomic() # room 생성
    def post(self, request, roomname):
        user1_username = request.POST.get('user1') # requset.user
        user2_username = request.POST.get('user2')
        room_status_param = request.POST.get('room_status')

        user1 = User.objects.get(username=user1_username)
        user2 = User.objects.get(username=user2_username)
        room_status = Status.objects.get(status=room_status_param)
        
        # Room이 존재하여 조회
        try:
            room = Room.objects.get(Q(user1 = user1, user2 = user2) | Q(user1 = user2 , user2 = user1))# name=roomname
            roomname = str(room.name)
            # Room의 현재 상태가 Pending 일 경우 Status Update X
            if str(room.status) == constants.ROOM_STATUS_PENDING:
                # 대화 재요청 => room 나간 사람이 요청
                if room.status_update_user.username == user1_username:
                    Room.objects.filter(id=room.id)\
                                .update(status=room_status, status_update_user = user1,
                                        lasted_time=datetime.now())
                # 안나간 사람이 요청
                else: # room.status.status_update_user.username == user2_username
                    pass
            # Room이 존재하지면 Status가 Start나 Stop일 때
            else:
                Room.objects.filter(id=room.id)\
                            .update(status=room_status, status_update_user = user1,
                                    lasted_time=datetime.now())
        # Room이 존재 하지 않으면 생성
        except Room.DoesNotExist:
            roomname = uuid.uuid4()
            room = Room(name = roomname, 
                        user1 = user1, user2 = user2,
                        status=room_status, status_update_user = user1,
                        lasted_time=datetime.now(), lasted_message='')
            room.save()
            return Response({"message": "Room does not exist and was Created", "uuid_roomname":roomname}, status=status.HTTP_201_CREATED)
        return Response({"message": "Room is existed and Status Updated", "uuid_roomname":roomname}, status=status.HTTP_200_OK)

    @query_debugger
    @transaction.atomic() # room 삭제
    def delete(self, request, roomname):
        room = Room.objects.get(name=roomname)
        room_status_param = str(room.status.status)
        update_user = User.objects.get(username = request.user.username)

        # Status가 START / STOP시 PENDING 으로 (한명이 ROOM 나간 경우)
        if (room_status_param == constants.ROOM_STATUS_START) or (room_status_param== constants.ROOM_STATUS_STOP):
            room_status_param = constants.ROOM_STATUS_PENDING
            room_status = Status.objects.get(status=room_status_param)
            print('room_status 변경', room_status)
            Room.objects.filter(id=room.id)\
                        .update(status=room_status, status_update_user = update_user, lasted_time=datetime.now())
        # Status가 PENDING시 ROOM 삭제
        elif room_status_param == constants.ROOM_STATUS_PENDING:
            print('room_status 삭제')
            room.delete()
            
        return Response({"message": "Room is removed"}, status=status.HTTP_200_OK)


''' room status case 
최초 room 생성시 : start
한명/두명 연결 되어 있을 때 : start
한명이 창을 닫거나, 두명이 창을 닫으면 : stop => 메시지 보내기 가능 
한명이 삭제를 했음 : pending => 추가 메시지 보내기는 안되고 읽기만 가능한 상태.
두명이 삭제를 했음 : 현재 상태가 pending일 떄 remove 요청시 삭제
'''
# START -> STOP or STOP => START
# 채팅방이 Pending 되면 더이상 Status 관리 X
# chat/rooms/<str:roomname>/status/
class ChatRoomStatusView(APIView):
    @query_debugger
    @transaction.atomic()
    def put(self, request, roomname): # ROOM 상태 변경
        room_status_param = request.POST.get('room_status') 
        room = Room.objects.get(name=roomname) # room 조회 후 PENDING 상태면

        # Pending 이면 관리 X
        if str(room.status.status) == constants.ROOM_STATUS_PENDING:
            pass
        else: # START나 STOP
            update_user = User.objects.get(username = request.user.username)
            room_status = Status.objects.get(status = room_status_param)
            Room.objects.filter(id=room.id)\
                        .update(status = room_status, status_update_user = update_user, lasted_time=datetime.now())
        return Response({"message": "Room Status Updated"}, status=status.HTTP_200_OK)

# chats/rooms/<str:roomname>/messages/
class ChatRoomMessagesView(APIView):
    @query_debugger
    def get(self, request, roomname):
        # room, send_user, receive_user, send_time, message,
        room = Room.objects.get(name=roomname)

        chat_messages_data = ChatRoomMessagesSerializer(room).data
        return Response(chat_messages_data, status=status.HTTP_200_OK)

# chats/messages/
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