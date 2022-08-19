from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserRegistrationSerializer,
    UserChangePasswordSerializer,
    CustomTokenObtainPairSerializer
)


class RegistrationAPIView(APIView):
    
    def post(self, request):
        data = request.data
        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            
            return Response(
                "Пользователь создан",
                status=status.HTTP_201_CREATED
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login view of simplejwt"""

    serializer_class = CustomTokenObtainPairSerializer


class UserChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        serializer = UserChangePasswordSerializer(data=data, context={"user": user})

        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data.get('new_password'))
            user.save()

            return Response(
                "Password was changed",
                status=status.HTTP_200_OK
            )