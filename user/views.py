from django.shortcuts import redirect
import urllib
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User as UserModel
from .serializers import UserSerializer, UserJoinSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import my_settings


# 회원가입
class JoinView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        if not request.data["email"] and request.data["password"] and request.data["username"]:
            return Response({"errors": "가입정보를 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)
        
        join_serializer = UserJoinSerializer(data=request.data)
        if join_serializer.is_valid():
            join_serializer.save()
            return Response({"user" : join_serializer.data, "msg" : "회원가입 완료"}, status=status.HTTP_201_CREATED)
        return Response(join_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    # 로그인 한 유저 정보 출력
    def get(self, request):
        user_serializer = UserSerializer(
            request.user, context={"request": request}
        ).data
        return Response(user_serializer, status=status.HTTP_200_OK)
    
    # 로그인
    def post(self, request):
        pass


# code 요청
def kakao_login(request):
    rest_api_key = my_settings.KAKAO['REST_API_KEY']
    redirect_uri = "http://127.0.0.1:8000/account/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )
    
# access token 요청
def kakao_callback(request):                                                                  
    params = urllib.parse.urlencode(request.GET)                                      
    return redirect(f'http://127.0.0.1:8000/account/login/kakao/callback?{params}')   