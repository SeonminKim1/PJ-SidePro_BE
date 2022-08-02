from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Skills 
from .models import User as UserModel
from .models import UserProfile as UserProfileModel
from .serializers import UserSerializer, UserJoinSerializer, UserProfileDetailSerializer
from .serializers import SkillsSerializer

from project.models import Project as ProjectModel
from project.serializers import ProjectViewSerializer

# 예외 처리를 위한 import
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

# S3 업로드 관련 import
import boto3
import os
from django.utils import timezone


# user/upload/
class UploadS3(APIView):
    # S3에 이미지 업로드 후 URL 리턴
    def post(self, request):
        print(request)
        file = request.data["file"]
        
        s3 = boto3.client('s3',
                          aws_access_key_id = os.environ.get("AWS_ACCESS_KEY"),
                          aws_secret_access_key = os.environ.get("AWS_SECRET_KEY"),
                          region_name = os.environ.get("REGION_NAME"),
                          )
        
        file_name = str(file).split('.')[0]
        file_extension = str(file).split('.')[1]
        file_name = f"{file_name}_{timezone.now().strftime('%Y-%m-%d_%H:%M:%S')}"

        s3.put_object(
            ACL="public-read",
            Bucket = os.environ.get("AWS_BUCKET_NAME"),
            Body=file,
            Key='user-imgs/' + file_name + '.' + file_extension,
            ContentType=file.content_type
            )
        
        url =  "https://" + os.environ.get("AWS_BUCKET_NAME") + ".s3.ap-northeast-2.amazonaws.com/"+ 'user-imgs/' + file_name + '.' + file_extension        
        return Response({"success":"S3 업로드 성공!", "url": url})


# user/join/
class JoinView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        join_serializer = UserJoinSerializer(data=request.data)
        if join_serializer.is_valid():
            join_serializer.save()
            return Response({"user" : join_serializer.data, "msg" : "회원가입 완료"}, status=status.HTTP_201_CREATED)
        return Response(join_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user/profile/
class UserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 로그인한 유저 정보 출력
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 유저프로필 등록
    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = UserProfileDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 로그인한 유저프로필 수정
    def put(self, request):
        try:
            user = UserProfileModel.objects.get(user_id=request.user.id)
            serializer = UserProfileDetailSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise Http404("해당 유저를 찾을 수 없습니다.")
    
    # 유저 탈퇴
    def delete(self, request):
        try:
            UserModel.objects.get(id=request.user.pk).delete()
            return Response({"msg": "탈퇴가 완료되었습니다.\n그동안 이용해주셔서 감사합니다.\n더 좋은 서비스로 찾아뵙겠습니다."}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise Http404("해당 유저를 찾을 수 없습니다.")



# user/profile/<user_id>
class AnotherUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 다른 유저 정보 보기
    def get(self, request, user_id):
        try:
            user = UserModel.objects.select_related("userprofile").get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise Http404('해당 유저를 찾을 수 없습니다')


# user/profile/project/
class MyProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 나의 프로젝트 출력
    def get(self, request):
        project = ProjectModel.objects.filter(user_id=request.user.pk)
        project_serializer = ProjectViewSerializer(project, many=True)
        return Response(project_serializer.data, status=status.HTTP_200_OK)
    
    
# user/profile/project/bookmark
class MyBookmarkProjectView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # 내가 북마크한 프로젝트 출력
    def get(self, request):
        project = ProjectModel.objects.filter(bookmark=request.user.pk)
        project_serializer = ProjectViewSerializer(project, many=True)
        return Response(project_serializer.data, status=status.HTTP_200_OK)


# user/info/
class GetLoginUserInfoView(APIView):
    def get(self, request):
        return Response({"login_username": request.user.username}, status=status.HTTP_200_OK)

# user/main/init/
class GetBaseInfoView(APIView):
    def get(self, request):
        skills = Skills.objects.all()
        skills_data = SkillsSerializer(skills, many=True).data
        return Response({"login_username": request.user.username, "skills":skills_data}, status=status.HTTP_200_OK)