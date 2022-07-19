# chat/models.py
from django.db import models
from user.models import User
from chat import constants

# 채팅방 상태
class Status(models.Model):
    # start, pending, stop
    status = models.CharField(choices=constants.STATUS_CHOICE, verbose_name="채팅방 상태", max_length=20)
    
    def __str__(self):
        return self.status

    class Meta:
        db_table = "STATUS"

# 채팅방 정보
class Room(models.Model):
    name = models.CharField(verbose_name="방이름", max_length=30)
    user1 = models.ForeignKey(User, verbose_name="본인", related_name = "owner", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, verbose_name="채팅상대", related_name = "opponent", on_delete=models.CASCADE)
    status = models.ForeignKey(Status, verbose_name="채팅방 상태", on_delete=models.CASCADE)
    lasted_time = models.DateTimeField("마지막 메시지 시간", auto_now=True)
    lasted_message = models.TextField("마지막 메세지")
    
    def __str__(self):
        return f"{self.user1.username}, {self.user2.username}의 채팅방"

    class Meta:
        db_table = "ROOM"
    
# 채팅방 내용
class Chat(models.Model):
    room = models.ForeignKey(Room, verbose_name="채팅방 정보", on_delete=models.CASCADE)
    send_user = models.ForeignKey(User, verbose_name="보낸이", related_name = "send_user", on_delete=models.CASCADE)
    receive_user = models.ForeignKey(User, verbose_name="받은이", related_name = "receive_user", on_delete=models.CASCADE)
    send_time = models.DateTimeField("보낸일시", auto_now=True)
    message = models.TextField("메세지")

    class Meta:
        db_table = "CHAT"