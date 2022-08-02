from rest_framework import serializers

from project.serializers import ProjectSerializer

from .models import User as UserModel
from .models import UserProfile as UserProfileModel
from .models import Skills


class UserProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    meet_time = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()

    def get_skills(self, obj):
        return [skills.name for skills in obj.skills.all()]
    
    def get_meet_time(self, obj):
        return obj.meet_time.time_type
    
    def get_region(self, obj):
        return obj.region.name
    
    class Meta:
        model = UserProfileModel
        fields = [
            "description",
            "profile_image",
            "github_url",
            "skills",
            "meet_time",
            "region",
        ]
        

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    
    class Meta:
        model = UserModel
        fields = [
            "email",
            "username",
            "join_date",
            "userprofile",
        ]


class UserJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"
    
    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, *args, **kwargs):
        user = super().update(*args, **kwargs)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = "__all__"
        
class AnotherUserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    user_project = serializers.SerializerMethodField()
    def get_user_project(self, obj):
        project_list = []
        projects = obj.project_set.filter(user__id=obj.pk)
        for project in projects:
            data = {
                "id" : project.id,
                "title" : project.title,
                "description" : project.description,
                "thumnail_img_path" : project.thumnail_img_path,
                "count" : project.count,
                "bookmark_count" : project.bookmark_count,
                "comment_count" : project.comment_count,
                "skills": skills
            }
            project_list.append(data)
        return project_list
    
    # user_bookmark = serializers.SerializerMethodField()
    # def get_user_bookmark(self, obj):
    #     project_list = []
    #     projects = obj.bookmark_set.filter(user__id=obj.pk)
    #     for project in projects:
    #         data = {
    #             "id" : project.id,
    #             "title" : project.title,
    #             "description" : project.description,
    #             "thumnail_img_path" : project.thumnail_img_path,
    #             "count" : project.count,
    #             "bookmark_count" : project.bookmark_count,
    #             "comment_count" : project.comment_count,
    #         }
    #         project_list.append(data)
    #     return project_list
    
    class Meta:
        model = UserModel
        fields = [
            "id",
            "email",
            "username",
            "user_project",
            # "user_bookmark",
            "userprofile",
            "join_date",
        ]
