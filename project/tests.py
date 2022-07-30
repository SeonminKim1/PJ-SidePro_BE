from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from faker import Faker

from django.test.utils import CaptureQueriesContext
from django.db import connection

from .models import Project
from user.models import Skills, User
from .serializers import ProjectDetailViewSerializer, ProjectSerializer

from _utils.query_utils import query_debugger

class ProjectReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {"email": "test@mail.com", "password":"test"}
        cls.user = User.objects.create_user("test@mail.com", "test")
        cls.faker = Faker()
        cls.projects = []
        Skills.objects.create(name="Python")
        for i in range(5):
            cls.user = User.objects.create_user(cls.faker.name(), cls.faker.word())
            instance = Project.objects.create(title=cls.faker.word(),
                                            description=cls.faker.word(),
                                            thumnail_img_path=cls.faker.sentence(),
                                            content=cls.faker.word(),
                                            user=cls.user,
                                            github_url="http://www.naver.com")
            instance.bookmark.set("")
            instance.skills.add(1)
            cls.projects.append(instance)
    
    # 게시물 리스트 출력                
    @query_debugger
    def test_get_project_list(self):
        with CaptureQueriesContext(connection) as ctx :    
            # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
            access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
            response = self.client.get(
                path=reverse("project_view"),
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            # print(response.data)
            self.assertEqual(response.status_code, 200)
            
            print("게시물 리스트 확인 쿼리", ctx.captured_queries)
            
    # 게시물 상세 조회
    @query_debugger        
    def test_get_project(self):
        with CaptureQueriesContext(connection) as ctx :    
            # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
            access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
            for project in self.projects:
                url = project.get_absolute_url()
                
                response = self.client.get(
                    path = url,
                    HTTP_AUTHORIZATION = f"Bearer {access_token}"
                )
                # print(response.data)
                self.assertEqual(response.status_code, 200)
                
            print("게시물 상세조회 쿼리", ctx.captured_queries)
            
        
    # 북마크 클릭 시
    @query_debugger
    def test_bookmark(self):
        with CaptureQueriesContext(connection) as ctx :    
            # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
            access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
            url = reverse("bookmark", kwargs={'project_id': 1})
            data = {"project_id" : 1}
            response = self.client.post(
                url,
                data,
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            print(response.data)
            self.assertEqual(response.status_code, 200)
                
            print("북마크 쿼리", ctx.captured_queries)
    