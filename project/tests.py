from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from faker import Faker
import json

from django.test.utils import CaptureQueriesContext
from django.db import connection

from .models import Project
from user.models import Skills, User

from _utils.query_utils import query_debugger

class ProjectReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {"email": "test@mail.com", "password":"test"}
        cls.user = User.objects.create_user("test@mail.com", "test")
        cls.faker = Faker()
        cls.projects = []
        Skills.objects.create(name="Python")
        for i in range(1):
            cls.user = User.objects.create_user(cls.faker.name(), cls.faker.word())
            for i in range(10):
                instance = Project.objects.create(title=cls.faker.word(),
                                                description=cls.faker.word(),
                                                thumnail_img_path=cls.faker.sentence(),
                                                content=cls.faker.word(),
                                                user=cls.user,
                                                github_url="http://www.naver.com")
                instance.bookmark.set(cls.user.username)
                instance.skills.add(1)
                cls.projects.append(instance)
    
    # 게시물 리스트 출력                
    @query_debugger
    def test_get_project_list(self):
        # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx :    
            response = self.client.get(
                path=reverse("project_view"),
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            # print(response.data)
            self.assertEqual(response.status_code, 200)
            
            print("게시물 리스트 확인 쿼리", json.dumps(ctx.captured_queries, indent=3))
    
    # 게시글 쓰기
    @query_debugger
    def test_post_project(self):
        # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx :    
            url = reverse("project_view")
            data = {"title":self.faker.word(),
                    "description":self.faker.word(),
                    "thumnail_img_path":self.faker.sentence(),
                    "content":self.faker.word(),
                    "user":self.user,
                    "github_url":"http://www.naver.com",
                    "skills": 1}
            response = self.client.post(
                url,
                data,
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            print(response.data)
            self.assertEqual(response.status_code, 200)
                
            print("게시물 쓰기 쿼리", json.dumps(ctx.captured_queries, indent=3))
    
    # 게시물 상세 조회
    @query_debugger        
    def test_get_project(self):
        # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx :
            project = self.projects[0]
            url = project.get_absolute_url()
            
            response = self.client.get(
                path = url,
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            # print(response.data)
            self.assertEqual(response.status_code, 200)
            
        print("게시물 상세조회 쿼리", json.dumps(ctx.captured_queries, indent=3))
            
    # 게시글 수정
    @query_debugger        
    def test_put_project(self):
        # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx :    
            url = reverse("project_detail_view", kwargs={"project_id": 1})
            data = {"title": "바꾼 제목"}
            response = self.client.put(
                url,
                data,
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            print(response.data)
            self.assertEqual(response.status_code, 200)
                
            print("게시물 수정 쿼리", json.dumps(ctx.captured_queries, indent=3))
            
    # 댓글 작성
    @query_debugger        
    def test_post_comment(self):
        # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx :    
            url = reverse("comment_view", kwargs={"project_id": 1})
            data = {"comment": "댓글 내용"}
            response = self.client.post(
                url,
                data,
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            print(response.data)
            self.assertEqual(response.status_code, 200)
                
            print("댓글 작성 쿼리", json.dumps(ctx.captured_queries, indent=3))
            
        
    # 북마크 클릭 시
    @query_debugger
    def test_bookmark(self):
         # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx :    
            url = reverse("bookmark", kwargs={'project_id': 1})
            data = {"project_id" : 1}
            response = self.client.post(
                url,
                data,
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            print(response.data)
            self.assertEqual(response.status_code, 200)
                
            print("북마크 쿼리",  json.dumps(ctx.captured_queries, indent=3))
    