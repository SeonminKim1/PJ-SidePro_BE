from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

import random
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from user.models import Skills, UserProfile
from project.models import Comment, Project

from .serializers import UserProfileSkillsSerializer, RecommendProjectsSerializer

from _utils.query_utils import query_debugger # Query Debugger
from .ai import user_based 

# userprofile 업데이트 하면 추천 리스트 업데이트
class RecommendView(APIView):
    # @query_debugger
    def get(self, request):
        # 로컬이면 crontab없이 진행
        if os.environ.get('IS_LOCAL')=='TRUE':
            from .cron import recommend_crontab
            recommend_crontab()

        # 최적화 전 Query 코드
        optimize_query = 1
        if optimize_query:
            user_based_collab = user_based.RecommendUserProject()
            print('===views', user_based_collab)

            jaccard_score_df = user_based_collab.jaccard_score_df
            
            # 3. 자카드 유사도 가장 높은 User N명 출력
            user_id_list, jaccard_score_dict = user_based_collab.get_jaccard_user_id_list(jaccard_score_df, request.user.id)

            # 4. 최종 user들의 project 가져오기
            project_querysets = Project.objects.select_related('user').prefetch_related('skills', 'bookmark', 'comment_set')\
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
            user_id_list, jaccard_score_dict = user_based_collab.get_jaccard_user_id_list(jaccard_score_df, request.user.id)
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
