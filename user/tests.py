import json
from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase
from rest_framework import status

from _utils.query_utils import query_debugger
from project.models import Project
from .models import MeetTime, Region, Skills, User, UserProfile

from django.test.utils import CaptureQueriesContext
from django.db import connection

# 회원가입 테스트
class UserRegistrationTest(APITestCase):
    # 모든 테스트 시작 전 호출되는 함수
    def setUp(self):
        self.data = {"email": "test@mail.com", "password":"test"}
        self.user = User.objects.create_user("test@mail.com", "test")
        
    # 모든 테스트 마지막 호출 되는 함수
    def tearDown(self):
        pass
    
    # 중복된 아이디로 회원가입 시 (400)
    def test_registration_duplicate(self):
        url = reverse("join_view")
        user_data = {
            "email" : "test@mail.com",
            "username": "중복",
            "password": "test",
            "password_confirm": "test"
        }
        response = self.client.post(url, user_data)
        # print(response.data)
        self.assertEqual(response.status_code, 400)
        
    # 정상적인 회원가입 (201)
    def test_registration(self):
        url = reverse("join_view")
        user_data = {
            "email" : "newtest@mail.com",
            "username": "패스",
            "password": "newtest",
            "password_confirm": "newtest"
        }
        response = self.client.post(url, user_data)
        # print(response.data)
        self.assertEqual(response.status_code, 201)
        
# 로그인 테스트
class LoginUserTest(APITestCase):
    # 로그인 테스트할 계정
    def setUp(self):
        self.data = {"email": "test@mail.com", "password":"test"}
        self.data_none_pwd = {"email": "test@mail.com"}
        self.data_none_email = {"password":"test"}
        self.user = User.objects.create_user("test@mail.com", "test")
        
    # 정상 로그인
    @query_debugger
    def test_login(self):
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.post(reverse("token_obtain_pair"), self.data)
            # print(response.data["access"])
            self.assertEqual(response.status_code, 200)
            print("로그인 성공 쿼리", ctx.captured_queries)
    
    # 패스워드 없을 경우
    def test_login_miss_pwd(self):
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.post(reverse("token_obtain_pair"), self.data_none_pwd)
            self.assertEqual(response.status_code, 400)
        
    # 아이디 없을 경우
    def test_login_miss_email(self):
        response = self.client.post(reverse("token_obtain_pair"), self.data_none_email)
        self.assertEqual(response.status_code, 400)
        
    # 유저 정보 확인
    @query_debugger
    def test_get_user_data(self):
        # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(
                path=reverse("user_view"),
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            print(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data['email'], self.data['email'])
            print("유저 확인 쿼리", ctx.captured_queries)

class UserProfileTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {"email": "test@mail.com", "password":"test"}
        cls.user = User.objects.create_user("test@mail.com", "test")
        cls.faker = Faker()
        
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
                
        cls.skills = Skills.objects.create(name = 'Python') # SKILLS 129
        cls.meettime = MeetTime.objects.create(time_type = '상관 없음') # 3
        cls.region = Region.objects.create(name = '서울특별시') # 17
        cls.userprofile = UserProfile.objects.create(
                user = cls.user,            
                description=cls.faker.word(),
                profile_image = cls.faker.sentence(),
                github_url = "http://www.naver.com",
                meet_time = cls.meettime,
                region = cls.region
            )
        cls.userprofile.skills.add(1)
                    
        
    @query_debugger
    def test_userprofile_post(self):
        # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx:
            url = reverse("user_view")
            data = {"decription": self.faker.word(),
                    "skills": 1, 
                    "meet_time": 1, 
                    "region": 1}
            response = self.client.post(
                url,
                data,
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            print(response.data)
            self.assertEqual(response.status_code, 200)
            print("프로필 등록 쿼리", json.dumps(ctx.captured_queries, indent=3))
            
    # @query_debugger
    # def test_userprofile_put(self):
    #     # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
    #     access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
    #     response = self.client.post(reverse("token_obtain_pair"), self.data)
    #     with CaptureQueriesContext(connection) as ctx:
    #         url = reverse("user_view")
    #         data = {"decription": self.faker.word()}
    #         response = self.client.put(
    #             url,
    #             data,
    #             HTTP_AUTHORIZATION = f"Bearer {access_token}"
    #         )
    #         print(response.data)
    #         self.assertEqual(response.status_code, 200)
    #         print("프로필 수정 쿼리", json.dumps(ctx.captured_queries, indent=3))
    
    # 나의 프로젝트 출력
    @query_debugger
    def test_my_project_view(self):
        # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx:
            url = reverse("my_project_view")
            response = self.client.get(
                url,
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            print(response.data)
            self.assertEqual(response.status_code, 200)
            print("나의 프로젝트 출력 쿼리", json.dumps(ctx.captured_queries, indent=3))
    
    @query_debugger
    def test_my_bookmark_project_view(self):
        # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx:
            url = reverse("my_bookmark_project_view")
            response = self.client.get(
                url,
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            print(response.data)
            self.assertEqual(response.status_code, 200)
            print("북마크한 프로젝트 출력 쿼리", json.dumps(ctx.captured_queries, indent=3))
            
    
    @query_debugger
    def test_another_userprofile(self):
        # 액세스 토큰을 받아와서 HTTP_AUTHORIZATION에 주는 것이 중요!
        access_token = self.client.post(reverse("token_obtain_pair"), self.data).data['access']
        with CaptureQueriesContext(connection) as ctx:
            url = reverse("another_user_view", kwargs={"user_id":self.user.pk})
            response = self.client.get(
                url,
                HTTP_AUTHORIZATION = f"Bearer {access_token}"
            )
            print(response.data)
            self.assertEqual(response.status_code, 200)
            print("다른 유저 프로필 출력 쿼리", json.dumps(ctx.captured_queries, indent=3))