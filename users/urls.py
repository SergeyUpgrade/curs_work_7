from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(permission_classes=(AllowAny,)), name='register'),
    path("user/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("user/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-retrieve"),

    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

]
