# user/models.py
from ast import Constant
from asyncio import constants
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from user import constants

class MeetTime(models.Model):        
    # 주중 선호, 주말 선호, 상관없음
    TIME_CHOICE = constants.TIME_CHOICE
    time_type = models.CharField("선호 시간대", choices=TIME_CHOICE, max_length=50)

class Region(models.Model):
    REGION_CHOICE = constants.REGION_CHOICE
    name = models.CharField('활동지역', choices=REGION_CHOICE, max_length=50)

class Skills(models.Model):
    SKILLS_CHOICE = constants.SKILLS_CHOICE
    name = models.CharField('기술스택', choices=SKILLS_CHOICE, max_length=20)

# custom user model 사용 시 UserManager 클래스와 create_user, create_superuser 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email')
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField("이메일", max_length=150, unique=True)
    password = models.CharField("비밀번호", max_length=300)
    username = models.CharField("이름", max_length=30)
    join_date = models.DateTimeField("가입일", auto_now_add=True)
    
    bookmark = models.ManyToManyField("project.Project", related_name="bookmarks")

    is_active = models.BooleanField(default=True) # 계정활성화 여부
    is_admin = models.BooleanField(default=False) # 관리자 계정 여부

    USERNAME_FIELD = 'email' # 로그인 시 사용할 필드 지정
    REQUIRED_FIELDS = [] # createsuperuser 할 때 추가로 요구할 필드 지정
    
    objects = UserManager() # custom user 생성 시 필요

    def __str__(self):
        return self.username

    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_perm(self, perm, obj=None):
        return True
    
    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False
    def has_module_perms(self, app_label): 
        return True
    
    # admin 권한 설정
    @property
    def is_staff(self): 
        return self.is_admin

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="유저",on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField("자기소개", null=True, blank=True)
    profile_image = models.FileField(null=True, blank=True)
    github_url = models.URLField(verbose_name = "GITHUB URL", null=True, blank=True)
    skills = models.ManyToManyField(Skills, verbose_name='기술 스택')
    meet_time = models.ForeignKey(MeetTime, verbose_name="가능시간", on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(Region, verbose_name="활동지역", on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.user.username