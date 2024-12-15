from rest_framework.serializers import ValidationError


def validate_periodicity(value):
    """ Проверка периодичности выполнения привычки, должно быть меньше одного раза в 7 дней """
    if value < 0 or value > 7:
        raise ValidationError("Частота выполнения привычки не может быть меньше 1 раз в 7 дней.")
    return value


def validate_time_to_complete(value):
    """ Проверка времени на выполнение привычки, не более 120 секунд"""
    if value >= 120:
        raise ValidationError("Время на выполнение не может превышать 120 секунд.")
    return value


class RewardValidate:
    """Проверка на наличие связанной привычки"""

    def __init__(self, field_1, field_2):
        self.field_1 = field_1
        self.field_2 = field_2

    def __call__(self, value):
        if dict(value).get(self.field_1) and dict(value).get(self.field_2):
            raise ValidationError("Нельзя одновременно указывать связанную привычку и вознаграждение.")


class IsGoodValidate:
    """ Проверка приятной привычки. """

    def __call__(self, value):
        if dict(value).get('is_good'):
            if dict(value).get('related_habit') or dict(value).get('award'):
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения или связанной привычки.")


class RelatedHabitValidate:
    """ Проверка связанной привычки. """

    def __call__(self, value):
        tmp_val = value.get('related_habit')
        if tmp_val and not tmp_val.is_good:
            raise ValidationError("Связанная привычка должна быть приятной.")
