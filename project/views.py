from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from django.db.models import Q
from django.db.models import F

from django.db import transaction

from user.models import Skills

from .models import Comment, Project
from .serializers import (CommentSerializer, 
                          ProjectSerializer, 
                          ProjectDetailSerializer, 
                          ProjectViewSerializer, 
                          ProjectDetailViewSerializer,
                          BaseCommentSerializer)

from django.db.models import Count
from django.utils import timezone

# S3 업로드 관련
import boto3
import os

# 페이지네이션 관련
from .pagination import PaginationHandlerMixin, BasePagination

# project/upload/
class UploadS3(APIView):
    # S3에 이미지 업로드 후 URL 리턴
    def post(self, request):
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
        Key='project-imgs/' + file_name + '.' + file_extension,
        ContentType=file.content_type)
        url =  "https://" + os.environ.get("AWS_BUCKET_NAME") + ".s3.ap-northeast-2.amazonaws.com/"+ 'project-imgs/' + file_name + '.' + file_extension
        return Response({"success":"업로드 성공!", "url": url})


# project/
class ProjectAPIView(APIView, PaginationHandlerMixin):
    pagination_class = BasePagination
    
    # 페이지네이션
    def pagination(self, project):
            page = self.paginate_queryset(project) # page_size, page에 따른 pagination 처리된 결과값
            # 페이징 처리가 된 결과가 반환되었을 경우
            if page is not None:
                # 페이징 처리된 결과를 serializer에 담아서 결과 값 가공
                project_serializer = self.get_paginated_response(ProjectViewSerializer(page, many=True).data)
            # 페이징 처리 필요 없는 경우
            else:
                project_serializer = ProjectViewSerializer(project, many=True)
                
            return Response(project_serializer.data, status=status.HTTP_200_OK)
    
    # 모든 게시물 출력
    def get(self, request):
        filter = request.GET.get("filter", None)
        skills = request.GET.getlist("skills", None)
        print(skills)
        # 검색
        if skills != None:
            q = Q()
            for skill in skills:
                q.add(Q(skills__name=skill), q.OR)
                project = Project.objects.filter(q)
                return self.pagination(project)
        # 필터링
        if filter == "views":
            project = Project.objects.select_related("user").prefetch_related("comment_set").prefetch_related("skills").prefetch_related("bookmark").all().order_by('-count')
            return self.pagination(project)
        elif filter == "newest":
            project = Project.objects.select_related("user").prefetch_related("comment_set").prefetch_related("skills").prefetch_related("bookmark").all().order_by('-created_date')
            return self.pagination(project)
        elif filter == "popular":
            project = Project.objects.select_related("user").prefetch_related("comment_set").prefetch_related("skills").prefetch_related("bookmark").all().order_by('-bookmark_count')                                 
            return self.pagination(project)
        else:
            project = Project.objects.select_related("user").prefetch_related("comment_set").prefetch_related("skills").prefetch_related("bookmark").all()
            # project = Project.objects.all()
            return self.pagination(project)
        
    # 게시글 쓰기
    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        project_serializer = ProjectSerializer(data=data)
        project_serializer.is_valid(raise_exception=True)
        project_serializer.save()
        return Response(project_serializer.data, status=status.HTTP_200_OK)

# project/<project_id>
class ProjectDetailAPIView(APIView):
    # 게시물 하나 자세히 보기
    def get(self, request, project_id):
        project = Project.objects.prefetch_related("comment_set","skills","bookmark").get(id=project_id)
        # project = Project.objects.get(id=project_id)
        # 조회수 증가
        project.count += 1
        project.save()        
        
        serializer = ProjectDetailViewSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 게시글 수정
    def put(self, request, project_id):
        project = Project.objects.select_related("user").prefetch_related("skills").prefetch_related("comment_set").prefetch_related("bookmark").get(id=project_id)
        # project = Project.objects.get(id=project_id)
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
    @transaction.atomic
    def post(self, request, project_id):
        data = request.data.copy()
        data["user"] = request.user.id
        data["project"] = project_id
        project = Project.objects.get(id=project_id)
        project.comment_count = F("comment_count") + 1
        project.save()
        serializer = BaseCommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # user 필드를 username으로 return 
        comment_serialize_data = serializer.data.copy()
        comment_serialize_data['user'] = request.user.username

        return Response ({'msg':'댓글 등록 성공', 'data':comment_serialize_data}, status=status.HTTP_200_OK)

# project/<projcet_id>/comment/<comment_id>
class CommentModifyAPIView(APIView):
    # 댓글 수정
    def put(self, request, project_id, comment_id):
        comment = Comment.objects.get(id=comment_id, project=project_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'댓글 수정 성공', 'data':serializer.data}, status=status.HTTP_200_OK)
    
    # 댓글 삭제
    @transaction.atomic
    def delete(self, request, project_id, comment_id):
        project = Project.objects.get(id=project_id)
        project.comment_count = F("comment_count") - 1
        project.save()
        Comment.objects.get(id=comment_id, project=project_id).delete()
        return Response({"success": "댓글이 삭제되었습니다!"}, status=status.HTTP_200_OK)

# project/<int:project_id>/bookmark/
class BookmarkAPIView(APIView):
    # 북마크 클릭 시
    @transaction.atomic
    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        bookmark = project.bookmark.all()
        if request.user in bookmark:
            project.bookmark_count =  F('bookmark_count') - 1
            project.bookmark.remove(request.user)
            # project.bookmark_count -= 1
            project.save()
            return Response({"msg": "북마크 해제 완료!"})
        else:
            project.bookmark_count = F("bookmark_count") + 1
            project.bookmark.add(request.user)
            # project.bookmark_count += 1
            project.save()        
        return Response({"msg": "북마크 등록 완료!"})