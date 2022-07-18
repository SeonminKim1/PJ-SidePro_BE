from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import Project
from .serializers import ProjectSerializer, ProjectDetailSerializer

import boto3

# project/upload/
class UploadS3(APIView):
    # S3에 이미지 업로드 후 URL 리턴
    def post(self, request):
        file = request.data["file"]
        print(file)
        s3 = boto3.client('s3')
        
        file_name = str(file).split('.')[0]
        file_extension = str(file).split('.')[1]
        
        s3.put_object(
        ACL="public-read",
        Bucket="toastuitestbucket",
        Body=file,
        Key=file_name,
        ContentType=file.content_type)
        url =  "https://toastuitestbucket.s3.ap-northeast-2.amazonaws.com/"+ file_name + '.' + file_extension
        return Response({"success":"업로드 성공!", "url": url})

# project/
class ProjectAPIView(APIView):
    # 모든 게시물 출력
    def get(self, request):
        project = Project.objects.all()
        project_serializer = ProjectSerializer(project, many=True)
        return Response(project_serializer.data, status=status.HTTP_200_OK)
    # 게시글 쓰기
    def post(self, request):
        request.data["user"] = request.user.id
        project_serializer = ProjectSerializer(data=request.data)
        project_serializer.is_valid(raise_exception=True)
        project_serializer.save()
        return Response(project_serializer.data, status=status.HTTP_200_OK)

# project/<int>
class ProjectDetailAPIView(APIView):
    def get(self, request, project_id):
        return Response()
    def put(self, request, project_id):
        return Response()
    def delete(self, request, project_id):
        return Response()