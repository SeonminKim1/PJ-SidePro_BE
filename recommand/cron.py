import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from user.models import UserProfile
from .serializers import UserProfileSkillsSerializer
from .ai import user_based 
import pandas as pd

# Recommand
def recommend_crontab():
    # 최적화 전 Query 코드
    optimize_query = 1    
    if optimize_query:
        # 1. 추천 시스템 최초 요청
        userinfo = UserProfile.objects.select_related('user').prefetch_related('skills').all()
        result = UserProfileSkillsSerializer(userinfo, many=True).data
        
        # 2. 기본 Base DF 만들기 (USER별 SKILLS 반영)
        base_df = user_based.make_df(result)

        # 3. 자카드 유사도 구하기
        jaccard_score_df = user_based.get_jaccard_score_df(base_df)
    else:
        userinfo = UserProfile.objects.all()
        result = UserProfileSkillsSerializer(userinfo, many=True).data
        base_df = user_based.make_df(result)
        jaccard_score_df = user_based.get_jaccard_score_df(base_df)
    try:
        jaccard_score_df.to_csv('recommend.csv')
        print('=========================')
        print('crontab 실행 결과 - 유사도 csv 저장 성공', jaccard_score_df.shape)
        print(jaccard_score_df)
        print('=========================')
    except:
        print('=========================')
        print('crontab 실행 결과 - 유사도 csv 저장 실패', jaccard_score_df.shape)
        print('=========================')

# if __name__ == "__main__":
#     pass
    # print(user_based_collab)