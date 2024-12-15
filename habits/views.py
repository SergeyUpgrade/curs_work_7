from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitsPagination
from habits.serializers import HabitSerializer, PublicHabitSerializer
from users.permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    """Позволяет автоматически реализовать стандартные методы CRUD для модели Habit"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitsPagination
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Привязывает привычку к пользователю при создании нового курса через API."""
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class PublicHabitListAPIView(generics.ListAPIView):
    """Вывод привычек с признаком публичный"""
    serializer_class = PublicHabitSerializer
    pagination_class = HabitsPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
