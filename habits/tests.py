from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.serializers import ValidationError
from habits.models import Habit
from habits.validators import validate_periodicity, validate_time_to_complete, RewardValidate, IsGoodValidate, \
    RelatedHabitValidate
from users.models import User
class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@test.ru')
        self.habit0 = Habit.objects.create(action='Связанная приятная привычка за выполнение', is_good=True)
        self.habit = Habit.objects.create(
            owner=self.user,
            action='Действие, которое надо сделать',
            time='12:30:00',
            place='Место для выполнения',
            periodicity=1,
            time_to_complete=120,
            is_good=False,
            is_public=True,
            related_habit=self.habit0,
            created_date='2024-11-21'
        )
        self.client.force_authenticate(user=self.user)
    def test_habit_create(self):
        """Тестирование POST-запроса к API - создание привычки"""
        url = reverse('habits:habit-list')
        data = {
            'action': 'Тестовое действие',
            'time': '12:30:00',
            'place': 'Тестовое место',
            'periodicity': 2,
            'time_to_complete': 100,
            'is_good': False,
            'is_public': True,
            'related_habit': self.habit0.pk,
            'created_date': '2024-11-21'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 3)
    def test_habit_list(self):
        """Тестирование GET-запроса к API - просмотра списка"""
        url = reverse('habits:habit-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.habit.pk,
                    'periodicity': self.habit.periodicity,
                    'time_to_complete': self.habit.time_to_complete,
                    'action': self.habit.action,
                    'time': self.habit.time,
                    'place': self.habit.place,
                    'is_good': False,
                    'is_public': True,
                    'award': None,
                    'created_date': self.habit.created_date,
                    'related_habit': self.habit.related_habit.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
    def test_habit_detail(self):
        """Тестирование GET-запроса к API - просмотра привычки"""
        url = reverse('habits:habit-detail', args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        result = {
            'id': self.habit.pk,
            'periodicity': self.habit.periodicity,
            'time_to_complete': self.habit.time_to_complete,
            'action': self.habit.action,
            'time': self.habit.time,
            'place': self.habit.place,
            'is_good': False,
            'is_public': True,
            'award': None,
            'created_date': self.habit.created_date,
            'related_habit': self.habit.related_habit.pk
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('action'), self.habit.action)
        self.assertEqual(data, result)
    def test_habit_update(self):
        """Тестирование PATCH-запроса к API - редактирование привычки"""
        url = reverse('habits:habit-detail', args=(self.habit.pk,))
        data = {
            'action': 'Новое действие, которое надо сделать'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('action'), 'Новое действие, которое надо сделать')
    def test_habit_delete(self):
        """Тестирование PATCH-запроса к API - удаление привычки"""
        url = reverse('habits:habit-detail', args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 1)
    def test_habit_public_list(self):
        """Тестирование GET-запроса к API - просмотра списка публичных привычек"""
        url = reverse('habits:public-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.habit.pk,
                    'is_owner': 'Моя привычка',
                    'action': self.habit.action,
                    'time': self.habit.time,
                    'place': self.habit.place,
                    'periodicity': self.habit.periodicity,
                    'time_to_complete': self.habit.time_to_complete,
                    'is_good': False,
                    'related_habit': {
                        'habit': str(self.habit0)
                    },
                    'award': None
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
class ValidatorTest(APITestCase):
    """Тестирование периодичности выполнения привычки"""
    def setUp(self):
        self.habit = {
            'action': 'Действие, которое надо сделать',
            'time': '12:30:00',
            'place': 'Место для выполнения',
            'periodicity': 1,
            'time_to_complete': 100,
            'is_good': False,
            'is_public': True,
            'created_date': '2024-11-21',
            'related_habit': {
                'action': 'Связанная приятная привычка за выполнение',
                'is_good': True
            },
            'award': None
        }
    def test_invalid_periodicity_too_low(self):
        """Тестирование значения меньше 0"""
        with self.assertRaises(ValidationError) as ve:
            validate_periodicity(-1)
        self.assertEqual(ve.exception.detail, [
            ErrorDetail("Частота выполнения привычки не может быть меньше 1 раз в 7 дней.", code='invalid')])
    def test_invalid_periodicity_too_high(self):
        """Тестирование значения больше 7"""
        with self.assertRaises(ValidationError) as ve:
            validate_periodicity(8)
        self.assertEqual(ve.exception.detail, [
            ErrorDetail("Частота выполнения привычки не может быть меньше 1 раз в 7 дней.", code='invalid')])
    def test_invalid_time_to_complete_too_high(self):
        """Тестирование значения больше или равно 120"""
        with self.assertRaises(ValidationError) as ve:
            validate_time_to_complete(130)
        self.assertEqual(ve.exception.detail,
                         [ErrorDetail("Время на выполнение не может превышать 120 секунд.", code='invalid')])
    def test_reward_validate_success(self):
        """Тестирование успешного случая, когда поля не указаны одновременно"""
        validator = RewardValidate('field_1', 'field_2')
        data = {'field_1': 'value', 'other_field': 'other_value'}
        try:
            validator(data)
        except ValidationError as e:
            self.fail("ValidationError raised unexpectedly")
    def test_reward_validate_failure(self):
        """Тестирование случая, когда поля указаны одновременно"""
        validator = RewardValidate('field_1', 'field_2')
        data = {'field_1': 'value', 'field_2': 'value'}
        with self.assertRaises(ValidationError) as ve:
            validator(data)
        self.assertEqual(ve.exception.detail, [
            ErrorDetail("Нельзя одновременно указывать связанную привычку и вознаграждение.", code='invalid')])
    def test_valid_is_good(self):
        """Тестирование когда приятная привычка без вознаграждения и связанной привычки"""
        validator = IsGoodValidate()
        data = {'is_good': True, 'related_habit': None, 'award': None}
        validator(data)
    def test_invalid_is_good_with_related_habit(self):
        """Тестирование когда приятная привычка с связанной привычкой"""
        validator = IsGoodValidate()
        data = {'is_good': True, 'related_habit': 'some_habit', 'award': None}
        with self.assertRaises(ValidationError) as ve:
            validator(data)
        self.assertEqual(ve.exception.detail, [
            ErrorDetail("У приятной привычки не может быть вознаграждения или связанной привычки.", code='invalid')])
    def test_invalid_is_good_with_award(self):
        """Тестирование когда приятная привычка с вознаграждением"""
        validator = IsGoodValidate()
        data = {'is_good': True, 'related_habit': None, 'award': 'some_award'}
        with self.assertRaises(ValidationError) as ve:
            validator(data)
        self.assertEqual(ve.exception.detail, [
            ErrorDetail("У приятной привычки не может быть вознаграждения или связанной привычки.", code='invalid')])
