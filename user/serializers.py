from rest_framework import serializers

from .models import User as UserModel
from .models import UserProfile as UserProfileModel

# from project.serializers import BookmarkSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    # meet_time = serializers.SerializerMethodField()
    # region = serializers.SerializerMethodField()

    def get_skills(self, obj):
        return [skills.name for skills in obj.skills.all()]
    
    # def get_meet_time(self, obj):
    #     return obj.meet_time.time_type
    
    # def get_region(self, obj):
    #     return obj.region.name
    
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


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    # bookmark = BookmarkSerializer(many=True)
    
    class Meta:
        model = UserModel
        fields = [
            "email",
            "password",
            "username",
            "join_date",
            # "bookmark",
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