from .ai import user_based 
user_based_collab = user_based.RecommendUserProject()
# print('===inint===', user_based_collab)

with open('log/init_user_based_collab.txt', 'a+'):
    print(user_based_collab)