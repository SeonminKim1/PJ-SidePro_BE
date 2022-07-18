from rest_framework import serializers
from .models import Project as ProjectModel
from .models import Comment as CommentModel

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = "__all__"

class ProjectDetailSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, source="comment_set")
    class Meta:
        model = ProjectModel
        fields = ["user", "title", "skills",
                  "thumnail_img_path", "content",
                  "count", "github_url", 
                  "created_date", "updated_date","comment"]
            
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectModel
        fields = "__all__"
            

            
            
            
            
            
            
            
            