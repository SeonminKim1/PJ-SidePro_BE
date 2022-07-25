from rest_framework import serializers

from user.models import User, UserProfile
from .models import Chat, Room

# 채팅 가능 Userlist Return Serializrs - 1 Userprofile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "profile_image",
            "github_url",
        ]

# 채팅 가능 Userlist Return Serializr - 2 User + Userprofile
class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    class Meta:
        model = User
        fields = [
            "username",
            "last_login",
            "userprofile",
        ]

# 채팅 가능 Userlist Return Serializrs - 3 Room + User + Userprofile
class ChatRoomUserlistSerializer(serializers.ModelSerializer):
    user1 = UserSerializer()
    user2 = UserSerializer()
    status_update_user = UserSerializer()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.status.status

    class Meta:
        model = Room
        fields = [
            "name",
            "user1",
            "user2",
            "status",
            "status_update_user",
            "lasted_time",
            "lasted_message",
        ]

# 채팅 내역 Return Serilaizers - 1 Chat
class ChatMessagesSerializer(serializers.ModelSerializer):
    send_user = serializers.SerializerMethodField()
    def get_send_user(self, obj):
        return obj.send_user.username  

    receive_user = serializers.SerializerMethodField()
    def get_receive_user(self, obj):
        return obj.receive_user.username  

    # last_mesaage 필요
    class Meta:
        model = Chat
        fields = [
            "send_user",
            "receive_user",
            "send_time",
            "message",
        ]

# 채팅 내역 Return Serilaizers - 2 Room + Chat
class ChatRoomMessagesSerializer(serializers.ModelSerializer):
    user1 = serializers.SerializerMethodField()
    def get_user1(self, obj):
        return obj.user1.username  

    user2 = serializers.SerializerMethodField()
    def get_user2(self, obj):
        return obj.user2.username  

    status = serializers.SerializerMethodField()
    def get_status(self, obj):
        return obj.status.status

    status_update_user = UserSerializer()

    chatmessages = ChatMessagesSerializer(many=True, source="chat_set")
    
    class Meta:
        model = Room
        fields = [
            "name", 
            "user1", 
            "user2", 
            "status", 
            "status_update_user",
            "lasted_time", 
            "lasted_message", 
            "chatmessages",
        ]
