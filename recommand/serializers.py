from attr import field
from rest_framework import serializers
from rest_pandas.serializers import PandasSerializer

from user.models import User, UserProfile, Skills
from project.models import Project, Comment

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"
        
class UserProfileSkillsSerializer(serializers.ModelSerializer):
    skills = SkillsSerializer
    class Meta:
        model = UserProfile
        list_serializer_class = PandasSerializer
        # fields = "__all__"
        fields = [
            "user",
            "skills",
        ]

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSkillsSerializer()
    
    class Meta:
        model = User
        fields = [
            "username",
            "userprofile",
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class RecommendProjectsSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.username 

    comment = CommentSerializer(many=True, source="comment_set")

    skills = serializers.SerializerMethodField()
    def get_skills(self, obj):
        return [skills.name for skills in obj.skills.all()]

    class Meta:
        model = Project
        fields = [
            'id',
            "user",
            "title", 
            "description", 
            "skills", 
            "thumnail_img_path", 
            "content", 
            "count", 
            "github_url", 
            "created_date", 
            "updated_date", 
            "bookmark",
            "comment",
        ] 