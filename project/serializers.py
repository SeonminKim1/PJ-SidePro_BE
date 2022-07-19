from rest_framework import serializers
from .models import Project as ProjectModel
from .models import Comment as CommentModel
from .models import Skills as SkillsModel

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.username
    class Meta:
        model = CommentModel
        fields = "__all__"

class ProjectDetailSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, source="comment_set")
    
    user = serializers.SerializerMethodField()
    def get_user(self, obj):
        return obj.user.username
    
    skills = serializers.SerializerMethodField()
    def get_skills(self, obj): 
        return [skills.name for skills in obj.skills.all()]
    class Meta:
        model = ProjectModel
        fields = ["user", "title", "skills",
                  "thumnail_img_path", "content",
                  "count", "github_url", 
                  "created_date", "updated_date","comment"]
            
class ProjectSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    def get_skills(self, obj): 
        return [skills.name for skills in obj.skills.all()]
    class Meta:
        model = ProjectModel
        fields = "__all__"

            
            
            
            
            
            
            
            