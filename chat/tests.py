from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.test import APITestCase
from rest_framework import status

from django.db import connection

from django.test.utils import CaptureQueriesContext
from faker import Faker
from _sidepro_BE.chat.constants import ROOM_STATUS_PENDING, ROOM_STATUS_RUNNING, ROOM_STATUS_STOP

from _utils.query_utils import query_debugger
from user.models import User, UserProfile, Skills, Region, MeetTime
from project.models import Project
from chat.models import Room, Chat, Status

from user.constants import SKILLS_CHOICE, REGION_CHOICE, TIME_CHOICE
from chat.constants import STATUS_CHOICE
import json
from datetime import datetime

class ChattingSystemTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.data = {"email": "test@mail.com", "password":"test", "username":"testuser"}
        self.faker = Faker()
        self.user_num = 100 # 100
        self.project_num = 10
        self.room_num = 100
        self.chat_num = 20
        # self.projects = []
        # self.userprofile = []
        # self.skills = Skills.objects.create(name = 'Python') # SKILLS 129
        # self.meettime = MeetTime.objects.create(time_type = '상관 없음') # 3
        # self.region = Region.objects.create(name = '서울특별시') # 17
        self.room_list = []
        # """
        for i in SKILLS_CHOICE:
            self.skills = Skills.objects.create(name = i[0]) # SKILLS 129
        for i in TIME_CHOICE:
            self.meettime = MeetTime.objects.create(time_type = i[0]) # 3
        for i in REGION_CHOICE:
            self.region = Region.objects.create(name = i[0]) # 17
        self.status = [Status.objects.create(status = i[0]) for i in STATUS_CHOICE]

        # """
        self.baseuser = User.objects.create_user(email = "test@mail.com", password="test")
        self.baseuser.username = "testuser"
        self.baseuser_userprofile = UserProfile.objects.create(
            user = self.baseuser, description=self.faker.word(),
            profile_image = self.faker.sentence(), github_url = "http://www.naver.com", meet_time = self.meettime, region = self.region
        )
        self.baseuser_userprofile.skills.add(self.skills)
        self.tempuser = User.objects.create(email = self.faker.name(), password=self.faker.word(), username=self.faker.name()) 
        for i in range(1, int(self.room_num/2)+1):
                self.user2 = User.objects.create(email = self.faker.name(), password=self.faker.word(), username=self.faker.name()) 
                userprofile = UserProfile.objects.create(user = self.user2, description=self.faker.word(),
                    profile_image = self.faker.sentence(), github_url = "http://www.naver.com", meet_time = self.meettime, region = self.region
                )
                self.user3 = User.objects.create(email = self.faker.name(), password=self.faker.word(), username=self.faker.name()) 
                userprofile = UserProfile.objects.create(user = self.user3, description=self.faker.word(),
                    profile_image = self.faker.sentence(), github_url = "http://www.naver.com", meet_time = self.meettime, region = self.region
                )
                room = Room.objects.create(
                    name = self.faker.word(),
                    user1 = self.user2,
                    user2 = self.user3,
                    status = self.status[1], # 0 : running / 1 : pending / 2 : stop
                    status_update_user = self.user2,
                )
                self.room_list.append(room)
                for j in range(0, int(self.chat_num/2)):
                    chat1 = Chat.objects.create(
                        room = room,
                        send_user = self.user2,
                        receive_user = self.user3,
                        message = self.faker.word()
                    )
                    chat2 = Chat.objects.create(
                        room = room,
                        send_user = self.user3,
                        receive_user = self.user2,
                        message = self.faker.word()
                    )

    '''
    @query_debugger
    def test_get_chat_room_list(self):
        with CaptureQueriesContext(connection) as ctx :    
            # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
            access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
            
            url = reverse("get_roomlist")            
            response = self.client.get(
                path = url + '?' + urlencode({'user_id': 1}),
                HTTP_AUTHORIZATION = f"Bearer {access_token}",
            )
            # print('===== 추천 결과는\n\n', response.data, )
            # self.assertEqual(response.status_code, 200)
            print("===쿼리", json.dumps(ctx.captured_queries, indent=3))
            print("===데이터, 쿼리 갯수", len(response.data), len(ctx.captured_queries))
    

    @query_debugger
    # chat/rooms/<str:roomname>/
    def test_post_delete_room(self):
        with CaptureQueriesContext(connection) as ctx :    
            # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
            access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']

            url = reverse("room", kwargs={'roomname': self.room_list[0].name}) # chat/rooms/<str:roomname>/
            case = 5
            # Case 1. ROOM이 있고, STATUS = STOP일 때 => RUNNING로 켜줌.
            if case==1:
                response = self.client.post(
                    path = url, 
                    data = {'user1': self.user2.username, 'user2':self.user3.username, 'room_status':ROOM_STATUS_STOP},
                    HTTP_AUTHORIZATION = f"Bearer {access_token}",
                )
            # Case 2. ROOM이 있고, STATUS = Pending 때 => RUNNING, user1이 status_update_user와 일치 할 때
            # => 위에 생성자에서 ROOM STATUS Pending으로 수정 필요
            elif case==2:
                response = self.client.post(
                    path = url, 
                    data = {'user1': self.user2.username, 'user2':self.user3.username, 'room_status':ROOM_STATUS_PENDING},
                    HTTP_AUTHORIZATION = f"Bearer {access_token}",
                )
            # Case 3. ROOM이 있고, STATUS = Pending 때 => RUNNING로, user1이 status_update_user와 일치 안할때
            # => 위에 생성자에서 ROOM STATUS Pending으로 수정 필요
            elif case==3:
                response = self.client.post(
                    path = url, 
                    data = {'user1': self.user3.username, 'user2':self.user2.username, 'room_status':ROOM_STATUS_PENDING},
                    HTTP_AUTHORIZATION = f"Bearer {access_token}",
                )
            # Case 4. ROOM존재 X ROOM 생성
            elif case==4:
                response = self.client.post(
                    path = url, 
                    data = {'user1': self.user2.username, 'user2':self.tempuser.username, 'room_status':ROOM_STATUS_STOP},
                    HTTP_AUTHORIZATION = f"Bearer {access_token}",
                )

            # Case 5. ROOM 삭제
            elif case==5:
                response = self.client.delete(
                    path = url, 
                    HTTP_AUTHORIZATION = f"Bearer {access_token}",
                )
            print("===쿼리", json.dumps(ctx.captured_queries, indent=3))
            print("===데이터, 쿼리 갯수", len(response.data), len(ctx.captured_queries))
    
    
    @query_debugger
    # chat/rooms/<str:roomname>/status/
    def test_put_room_status(self):
        with CaptureQueriesContext(connection) as ctx :    
            # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
            access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
            url = reverse("get_roomstatus", kwargs={'roomname': self.room_list[0].name}) 
            case = 1
            # Case 1. ROOM_STATUS가 RUNNING나 STOP인 경우 => STOP이나 RUNNING로 바꿔줌.
            # => 위에 생성자에서 ROOM STATUS RUNNING로 수정 필요
            if case==1:
                response = self.client.post(
                    path = url, 
                    data = {'room_status':ROOM_STATUS_STOP},
                    HTTP_AUTHORIZATION = f"Bearer {access_token}",
                )
            # Case 2. ROOM_STATUS가 PENDING인 경우 신경안씀.
            # => 위에 생성자에서 ROOM STATUS PENDING로 수정 필요
            elif case==2:
                response = self.client.post(
                    path = url, 
                    data = {'room_status':ROOM_STATUS_STOP},
                    HTTP_AUTHORIZATION = f"Bearer {access_token}",
                )
                
            print("===쿼리", json.dumps(ctx.captured_queries, indent=3))
            print("===데이터, 쿼리 갯수", len(response.data), len(ctx.captured_queries))
    

    @query_debugger
    # chat/rooms/<str:roomname>/messages/
    def test_get_room_messages(self):
        with CaptureQueriesContext(connection) as ctx :    
            # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
            access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
            url = reverse("get_room_messages", kwargs={'roomname': self.room_list[0].name}) 
            response = self.client.get(
                path = url, 
                HTTP_AUTHORIZATION = f"Bearer {access_token}",
            )                
            print("===쿼리", json.dumps(ctx.captured_queries, indent=3))
            print("===데이터, 쿼리 갯수", len(response.data), len(ctx.captured_queries))
    '''

    @query_debugger
    # chat/messages/
    def test_post_messages(self):
        with CaptureQueriesContext(connection) as ctx :    
            # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
            access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
            response = self.client.post(
                path = reverse("message"),
                data = {
                    'user1': self.user2.username,'user2': self.user3.username,'roomname': self.room_list[-1].name,
                    'send_time': datetime.now(),
                    'message': self.faker.word(),
                },
                HTTP_AUTHORIZATION = f"Bearer {access_token}",
            )                
            print("===쿼리", json.dumps(ctx.captured_queries, indent=3))
            print("===데이터, 쿼리 갯수", len(response.data), len(ctx.captured_queries))

