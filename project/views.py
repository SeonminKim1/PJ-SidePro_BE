from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import Comment, Project
from .serializers import CommentSerializer, ProjectSerializer, ProjectDetailSerializer

# S3 업로드 관련
import boto3
import my_settings

# 페이지네이션 관련
from .pagination import PaginationHandlerMixin, BasePagination

# project/upload/
class UploadS3(APIView):
    # S3에 이미지 업로드 후 URL 리턴
    def post(self, request):
        file = request.data["file"]
        print(file)
        # s3 = boto3.client('s3')
        
        s3 = boto3.client('s3', 
                          aws_access_key_id = my_settings.AWS_ACCESS_KEY,
                          aws_secret_access_key = my_settings.AWS_SECRET_KEY,
                          region_name = my_settings.REGION_NAME,
                          )
        
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
class ProjectAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasePagination
    
    # 모든 게시물 출력
    def get(self, request):
        project = Project.objects.all()
        page = self.paginate_queryset(project) # page_size, page에 따른 pagination 처리된 결과값
        # 페이징 처리가 된 결과가 반환되었을 경우
        if page is not None:
            # 페이징 처리된 결과를 serializer에 담아서 결과 값 가공
            project_serializer = self.get_paginated_response(ProjectSerializer(page, many=True).data)
        # 페이징 처리 필요 없는 경우
        else:
            project_serializer = ProjectSerializer(project, many=True)
            
        return Response(project_serializer.data, status=status.HTTP_200_OK)
            
    
    # 게시글 쓰기
    def post(self, request):
        request.data["user"] = 2
        project_serializer = ProjectSerializer(data=request.data)
        project_serializer.is_valid(raise_exception=True)
        project_serializer.save()
        return Response(project_serializer.data, status=status.HTTP_200_OK)

# project/<project_id>
class ProjectDetailAPIView(APIView):
    # 게시물 하나 자세히 보기
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 수정
    def put(self, request, project_id):
        project = Project.objects.get(id=project_id)
        serializer = ProjectDetailSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 삭제
    def delete(self, request, project_id):
        Project.objects.get(id=project_id).delete()
        return Response({"success": "게시글이 삭제되었습니다!"}, status=status.HTTP_200_OK)
    
# project/<project_id>/comment/
class CommentAPIView(APIView):
    # 댓글 작성
    def post(self, request, project_id):
        request.data["user"] = 2
        request.data["project"] = project_id
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response (serializer.data, status=status.HTTP_200_OK)

# project/<projcet_id>/comment/<comment_id>
class CommentModifyAPIView(APIView):
    # 댓글 수정
    def put(self, request, project_id, comment_id):
        comment = Comment.objects.get(id=comment_id, project=project_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 댓글 삭제
    def delete(self, request, project_id, comment_id):
        Comment.objects.get(id=comment_id, project=project_id).delete()
        return Response({"success": "댓글이 삭제되었습니다!"}, status=status.HTTP_200_OK)