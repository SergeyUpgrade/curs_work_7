from rest_framework import serializers

from habits.models import Habit
from habits.validators import validate_periodicity, validate_time_to_complete, RewardValidate, IsGoodValidate, \
    RelatedHabitValidate


class HabitSerializer(serializers.ModelSerializer):
    periodicity = serializers.IntegerField(validators=[validate_periodicity])
    time_to_complete = serializers.IntegerField(validators=[validate_time_to_complete])

    class Meta:
        model = Habit
        exclude = ['owner']
        validators = [
            RewardValidate(field_1='related_habit', field_2='award'),
            IsGoodValidate(),
            RelatedHabitValidate(),
        ]


class HabitRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('id', 'action', 'time', 'place', 'periodicity', 'time_to_complete', 'created_date')


class PublicHabitSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField(read_only=True)
    related_habit = HabitRelatedSerializer(read_only=True)

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user == obj.owner:
            return "Моя привычка"
        return "Не моя привычка"


    class Meta:
        model = Habit
        fields = ('id', 'is_owner', 'action', 'time', 'place', 'periodicity', 'time_to_complete', 'is_good', 'related_habit', 'award')
