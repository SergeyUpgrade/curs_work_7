from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import IsUser
from users.serializers import UserSerializer, UserNotOwnerSerializer


class UserCreateAPIView(CreateAPIView):
    """Регистрация пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    """Профиль пользователя"""
    queryset = User.objects.all()

    def get_serializer_class(self):
        """Если запрашивается свой профиль, используем полный сериализатор, иначе сокращенный сериализатор."""
        if self.request.user == self.get_object():
            return UserSerializer
        else:
            return UserNotOwnerSerializer


class UserUpdateAPIView(UpdateAPIView):
    """Редактирование профиля пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsUser)


class UserDestroyAPIView(DestroyAPIView):
    """Удалить пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsUser)
