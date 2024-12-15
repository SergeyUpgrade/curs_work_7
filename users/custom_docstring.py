from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Принимает набор учетных данных пользователя и возвращает пару веб-токенов access и refresh JSON
    для подтверждения аутентификации этих учетных данных.
    """
    permission_classes = [permissions.AllowAny]


class CustomTokenRefreshView(TokenRefreshView):
    """
    Принимает веб-токен типа обновления JSON и возвращает веб-токен типа доступа JSON,
    если токен обновления действителен.
    """
    permission_classes = [permissions.AllowAny]
