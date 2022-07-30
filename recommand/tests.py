from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from django.db import connection

from django.test.utils import CaptureQueriesContext
from faker import Faker

from _utils.query_utils import query_debugger
from user.models import User, UserProfile, Skills, Region, MeetTime
from project.models import Project

from user.constants import SKILLS_CHOICE, REGION_CHOICE, TIME_CHOICE
import json

class ProjectReadTest(APITestCase):
    @classmethod
    def setUpTestData(self):
        self.data = {"email": "test@mail.com", "password":"test"}
        self.faker = Faker()
        self.user_num = 100 # 100
        self.project_num = 10
        # self.projects = []
        # self.userprofile = []
        # self.skills = Skills.objects.create(name = 'Python') # SKILLS 129
        # self.meettime = MeetTime.objects.create(time_type = '상관 없음') # 3
        # self.region = Region.objects.create(name = '서울특별시') # 17
        # """
        for i in SKILLS_CHOICE:
            self.skills = Skills.objects.create(name = i[0]) # SKILLS 129
        for i in TIME_CHOICE:
            self.meettime = MeetTime.objects.create(time_type = i[0]) # 3
        for i in REGION_CHOICE:
            self.region = Region.objects.create(name = i[0]) # 17
        # """
        for i in range(1, self.user_num + 1):
            if i==1:
                user = User.objects.create_user("test@mail.com", "test")
            else:
                user = User.objects.create_user(self.faker.name(), self.faker.word())

            userprofile = UserProfile.objects.create(
                user = user,            
                description=self.faker.word(),
                profile_image = self.faker.sentence(),
                github_url = "http://www.naver.com",
                meet_time = self.meettime,
                region = self.region
            )
            userprofile.skills.add(i)
            
            for j in range(self.project_num):
                proj = Project.objects.create(
                    user=user,
                    title=self.faker.word(),
                    description=self.faker.word(),
                    thumnail_img_path=self.faker.sentence(),
                    content=self.faker.word(),
                    github_url="http://www.naver.com"
                )
                proj.bookmark.set("") # 
                for k in range(1, 21):
                    proj.skills.add(k) # index 번호
                # self.projects.append(proj)
            
    @query_debugger
    def test_get_recommend_project_list(self):
        with CaptureQueriesContext(connection) as ctx :    
            # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
            access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
            response = self.client.get(
                path=reverse("recommend_project_list"),
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            # print('===== 추천 결과는\n\n', response.data, )
            # self.assertEqual(response.status_code, 200)
            print("===쿼리", json.dumps(ctx.captured_queries, indent=3))
            print("===데이터, 쿼리 갯수", len(response.data), len(ctx.captured_queries))


            