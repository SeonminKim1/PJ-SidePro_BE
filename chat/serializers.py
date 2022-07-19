from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from .models import Chat, Room, Status

# 채팅 가능 Userlist Return Serializrs
class ChatUserProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    meet_time = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()

    def get_skills(self, obj):
        return [skills.name for skills in obj.skills.all()][:3]
    
    def get_meet_time(self, obj):
        return obj.meet_time.time_type
    
    def get_region(self, obj):
        return obj.region.name
    
    class Meta:
        model = UserProfileModel
        fields = [
            "profile_image",
            "skills",
            "meet_time",
            "region",
        ]

class ChatUserSerializer(serializers.ModelSerializer):
    userprofile = ChatUserProfileSerializer()
    # last_mesaage 필요
    class Meta:
        model = UserModel
        fields = [
            "username",
            "userprofile",
            "last_login",
        ]

# 채팅 내역 Return Serilaizers

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

    chatmessages = ChatMessagesSerializer(many=True, source="chat_set")
    
    class Meta:
        model = Room
        fields = [
            "name", 
            "user1", 
            "user2", 
            "status", 
            "lasted_time", 
            "lasted_message", 
            "chatmessages",
        ]
