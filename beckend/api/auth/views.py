from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from rest_framework import generics, permissions
from .serializers import ChangePasswordSerializer, LoginSerializer, ProfileSerializer, RegisterSerializer, UserProfileSerializer
from rest_framework.generics import GenericAPIView,UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import serializers

class LoginApiViews(GenericAPIView):
    serializer_class = [LoginSerializer, ProfileSerializer]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        user = authenticate(email=email, password=password)

        if not user:
            return Response(
                {"detail": "The user does not exist or the password is incorrect"},
                status.HTTP_401_UNAUTHORIZED,
            )
        
        read_serializer = self.get_serializer(index=1,instance=user)
        
        token = Token.objects.get_or_create(user=user)[0].key

        data = {**read_serializer.data, "token": token}

        return Response(data)

    def get_serializer(self, index=0, *args, **kwargs):

        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class[index](*args, **kwargs)
class RegisterApiView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = ProfileSerializer(user).data
            if user_data.get('avatar'):
                avatar_url = request.build_absolute_uri(user_data['avatar'])
                user_data['avatar'] = avatar_url

            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)

from rest_framework.authtoken.models import Token

class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = request.auth
            if token:
                token.delete()  
                return Response({"detail": "Вы успешно вышли из системы."}, status=status.HTTP_200_OK)
            return Response({"detail": "Токен не найден."}, status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, Token.DoesNotExist): 
            return Response({"detail": "Ошибка при выходе."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Метод GET не поддерживается для выхода. Используйте POST."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user 

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)