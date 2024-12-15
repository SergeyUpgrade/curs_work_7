from django.db import models
from django.utils import timezone


from config.settings import AUTH_USER_MODEL

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", **NULLABLE)
    action = models.CharField(max_length=100, verbose_name='Действие, которое надо сделать')
    time = models.TimeField(max_length=25, verbose_name='Время, когда необходимо выполнить привычку', **NULLABLE)
    place = models.CharField(max_length=100, verbose_name='Место')
    periodicity = models.PositiveSmallIntegerField(default=1, verbose_name='Периодичность выполнения, в днях')
    time_to_complete = models.PositiveSmallIntegerField(default=0, verbose_name='Время на выполнение, в секундах')
    is_good = models.BooleanField(default=False, verbose_name='Приятная привычка')
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      verbose_name='Связанная приятная привычка за выполнение', **NULLABLE)
    award = models.CharField(max_length=100, verbose_name='Вознаграждение за выполнение', **NULLABLE)
    created_date = models.DateField(default=timezone.now, verbose_name="Дата создания", **NULLABLE)

    def __str__(self):
        return f'я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
