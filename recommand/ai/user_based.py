
import pandas as pd
import sys, os
from sklearn.metrics import pairwise_distances

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from user import constants

JACCARD_SCORE_THRESHOLD = 0.1

def make_df(data):
    base_df = pd.DataFrame(index = data['user'], columns = range(1, len(constants.SKILLS_CHOICE)+1)).fillna(0)
    # base_df.to_csv('user_recommend.csv', index=False)
    # data.to_csv('result.csv', index=False)
    # base_df(User-Skills DF) 값 매핑해주기
    for idx in range(0, len(data)):
        row_data = data.loc[idx] # loc s는 index 따라감.
        user, skills_list = row_data['user'], row_data['skills'] # 1, '[17, 25, 34]'
        # skills = skills.replace('[', '').replace(']','').replace(' ','') # 17,25,34
        # skills_list = list(map(int, skills.split(','))) # [17, 25, 34]
        non_selected_skills_list = list(set(range(1, len(constants.SKILLS_CHOICE)+1)) - set(skills_list)) # [1,2, .., 16, 18, .., 24, ..]
        # print(user, skills_list, non_selected_skills_list)
        base_df.loc[user][skills_list] = 1
        base_df.loc[user][non_selected_skills_list] = 0
    return base_df


def get_jaccard_score_user_id_list(base_df, user_id):
    # get the pairwise Jaccard Similarity 
    jaccard_score_df = pd.DataFrame(1-pairwise_distances(base_df.values, metric='jaccard'), index=base_df.index, columns=base_df.index).applymap(lambda x:round(x, 3))
    jaccard_score_user_id_list = list(set(jaccard_score_df.loc[user_id][jaccard_score_df.loc[user_id]>=JACCARD_SCORE_THRESHOLD].index)- set([user_id]))
    return jaccard_score_user_id_list # [3,4]

if __name__ == '__main__':
    len(constants.SKILLS_CHOICE)

    data = pd.read_csv('result.csv')
    data.head()