from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from habits.models import Habit
from habits.services import send_tg_message, get_chat_id


@shared_task
def tg_reminder():
    """Отправка сообщения об обновлении курса по подписке"""
    current_date = timezone.now().date()
    reminder = timezone.now() + timedelta(minutes=1)  # интервал в 1 минуту для устранения погрешности из секунд

    # получаем список привычек пользователей подписанных на напоминания и сортируем по времени выполнения
    habits = Habit.objects.all().filter(owner__is_subscribe=True)

    # получаем список привычек требуемые выполнения в текущий день
    habits_by_date = [habit for habit in habits if
                      not (current_date - habit.created_date) % timedelta(days=habit.periodicity)]

    # получаем список привычек требуемые выполнения в текущее время и сортируем по времени выполнения
    habits_by_time = [habit for habit in habits_by_date if timezone.now().time() <= habit.time <= reminder.time()]
    habits_by_time.sort(key=lambda habit: habit.time)

    if habits_by_time:
        for habit in habits_by_time:
            print(f'Выполнить: {habit}')  # для тестирования планировщика

            if habit.owner.tg_id:
                chat_id = habit.owner.tg_id
            else:
                # Если telegramID не указан запрашиваем через Bot и сохраняем пользователю
                if habit.owner.tg_username:
                    chat_id = get_chat_id(habit.owner.tg_username)
                    user = habit.owner
                    user.tg_id = chat_id
                    user.save()

            text = f'Привычка "{habit.action}" запланирована сегодня на {habit.time}.'

            try:
                send_tg_message(text, chat_id)
            except Exception as e:
                print(f"Не удалось отправить сообщение на {chat_id}: {e}")
