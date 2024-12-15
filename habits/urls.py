from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, PublicHabitListAPIView

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r'habit', HabitViewSet, basename='habit')

urlpatterns = [
    path('public/', PublicHabitListAPIView.as_view(permission_classes=(AllowAny,)), name='public-list'),

] + router.urls
