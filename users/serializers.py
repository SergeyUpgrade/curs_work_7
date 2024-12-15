from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserNotOwnerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "date_joined")
