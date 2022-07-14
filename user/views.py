from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User as UserModel
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


# 회원가입
class UserAPIView(APIView):
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]
    
    # 로그인 한 유저 정보 출력
    def get(self, request):
        user = UserModel.objects.get(id=request.user.id)        
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
    
    # 회원가입
    def post(self, request):
        if not ('email' and 'password' and 'username' in request.data):
            return Response({"errors": "가입정보를 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data["password"] != request.data["password_confirm"]:
            return Response({"errors": "비밀번호를 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"user" : serializer.data, "msg" : "회원가입 완료"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
