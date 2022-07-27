from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from django.db.models import Q

from user.models import Skills, UserProfile
from project.models import Comment, Project

from .serializers import UserSkillsSerializer, RecommendProjectsSerializer
from .ai import user_based 


# userprofile 업데이트 하면 추천 리스트 업데이트
class RecommendView(APIView):
    def get(self, request):
        # 1. 추천 시스템 최초 요청
        userinfo = UserProfile.objects.all() # (user = request.user)
        result = UserSkillsSerializer(userinfo, many=True).data

        # 2. 기본 Base DF 만들기 (USER별 SKILLS 반영)
        base_df = user_based.make_df(result)

        # 3. 코사인 유사도 구하기 + 가장 높은 User 2~5명의 Project 전부 출력
        user_id_list = user_based.get_jaccard_score_user_id_list(base_df, request.user.id)

        # 4. 최종 user들의 project 가져오기
        project_querysets = Project.objects.filter(user__in = user_id_list)

        # 5. Serializers 결과를 가져옴.
        if len(project_querysets.values())>=2:
            rec_result_projects_data = RecommendProjectsSerializer(project_querysets, many=True).data
        else:
            rec_result_projects_data = RecommendProjectsSerializer(project_querysets).data

        return Response(rec_result_projects_data, status=status.HTTP_200_OK)
    