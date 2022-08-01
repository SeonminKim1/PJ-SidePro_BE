from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

import random

from user.models import Skills, UserProfile
from project.models import Comment, Project

from .serializers import UserProfileSkillsSerializer, RecommendProjectsSerializer
from .ai import user_based 

from _utils.query_utils import query_debugger # Query Debugger

# userprofile 업데이트 하면 추천 리스트 업데이트
class RecommendView(APIView):
    # @query_debugger
    def get(self, request):
        # 최적화 전 Query 코드
        optimize_query = 1
        if optimize_query:
            # 1. 추천 시스템 최초 요청
            userinfo = UserProfile.objects.select_related('user').prefetch_related('skills').all()
            result = UserProfileSkillsSerializer(userinfo, many=True).data

            # 2. 기본 Base DF 만들기 (USER별 SKILLS 반영)
            base_df = user_based.make_df(result)

            # 3. 코사인 유사도 구하기 + 가장 높은 User 2~5명의 Project 전부 출력
            user_id_list, jaccard_score_dict = user_based.get_jaccard_score_user_id_list(base_df, request.user.id)

            # 4. 최종 user들의 project 가져오기
            project_querysets = Project.objects.select_related('user').prefetch_related('skills', 'bookmark', 'comment')\
                .filter(user__in = user_id_list) # user
            project_querysets_list = list(project_querysets)

            # # 5. User들의 Project 중 랜덤 추출
            if len(project_querysets_list) >=3:
                project_querysets_random3_list = random.sample(project_querysets_list, 3)
            else: # 3개 미만이면 다시 랜덤 추출
                project_querysets = Project.objects.select_related('user').prefetch_related('skills', 'bookmark', 'comment_set')\
                    .exclude(user = request.user.id)
                project_querysets_list = list(project_querysets)
                project_querysets_random3_list = random.sample(project_querysets_list, 3)

            # 6. Serializers 결과 조회.
            rec_result_projects_data = RecommendProjectsSerializer(project_querysets_random3_list, many=True).data

        else:
            userinfo = UserProfile.objects.all()
            result = UserProfileSkillsSerializer(userinfo, many=True).data
            base_df = user_based.make_df(result)
            user_id_list, jaccard_score_dict = user_based.get_jaccard_score_user_id_list(base_df, request.user.id)
            project_querysets = Project.objects.filter(user__in = user_id_list)
            project_querysets_list = list(project_querysets)
            if len(project_querysets_list) >=3:
                project_querysets_random3_list = random.sample(project_querysets_list, 3)
            else:
                project_querysets = Project.objects.exclude(user = request.user.id)
                project_querysets_list = list(project_querysets)
                project_querysets_random3_list = random.sample(project_querysets_list, 3)
            rec_result_projects_data = RecommendProjectsSerializer(project_querysets_random3_list, many=True).data
        return Response({'results':rec_result_projects_data, 'scores':jaccard_score_dict}, status=status.HTTP_200_OK)
