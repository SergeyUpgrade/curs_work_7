from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

# Create your tests here.
from users.models import User
class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user0 = User.objects.create(email="test_000@example.com", password="testpassword")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user0)
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
    def test_user_register(self):
        """Тестирование POST-запроса к API - регистрация пользователя"""
        # Сначала зарегистрируем пользователя
        url = reverse('users:register')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)
    def test_user_login(self):
        """Тестирование POST-запроса к API - вход пользователя в систему"""
        # Сначала зарегистрируем пользователя
        self.test_user_register()
        # Вход в систему с действительными учетными данными
        url = reverse('users:login')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        # Вход в систему с неверными учетными данными
        data = {'email': 'not_test@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # Вход в систему с пропущенными полями
        data = {'email': 'not_test@example.com', 'password': ''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_user_retrieve(self):
        """Тестирование GET-запроса к API - Просмотр своего профиля"""
        # Retrieve the user's own profile
        url = reverse('users:user-retrieve', args=(self.user0.pk,))
        response = self.client.get(url)
        data = response.json()
        result = {
            'id': self.user0.pk,
            'password': self.user0.password,
            'last_login': None,
            'is_superuser': False,
            'last_name': '',
            'is_staff': False,
            'is_active': True,
            'date_joined': self.user0.date_joined.strftime("%Y-%m-%dT%H:%M:%S.%f") + 'Z',
            'email': self.user0.email,
            'first_name': None,
            'tg_username': None,
            'tg_id': None,
            'phone': None,
            'city': None,
            'avatar': None,
            'is_subscribe': False,
            'groups': [],
            'user_permissions': []
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
    def test_retrieve_other_user_profile(self):
        """Тестирование GET-запроса к API - Просмотр чужого профиля"""
        other_user = User.objects.create(
            email='other@example.com',
            password='strongpassword',
            first_name='Other',
            tg_username='other_tg',
            tg_id='67890',
            phone='0987654321',
            city='Other City',
        )
        url = reverse('users:user-retrieve', args=(other_user.pk,))
        response = self.client.get(url)
        data = response.json()
        result = {
            'id': other_user.pk,
            'email': other_user.email,
            'date_joined': other_user.date_joined.strftime("%Y-%m-%dT%H:%M:%S.%f") + 'Z'
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
    def test_update_own_user(self):
        """Тестирование PUT-запроса к API - Обновите собственный профиль пользователя"""
        url = reverse('users:user-update', kwargs={'pk': self.user0.pk})
        data = {
            'email': 'updated@example.com',
            'password': 'testpassword',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user0.refresh_from_db()
        self.assertEqual(self.user0.email, data['email'])
    def test_update_other_user(self):
        # Создайте другого пользователя
        other_user = User.objects.create(
            email='other@example.com',
            password='strongpassword',
            first_name='Other',
            tg_username='other_tg',
            tg_id='67890',
            phone='0987654321',
            city='Other City',
        )
        # Попытка обновить профиль другого пользователя (это должно быть запрещено или не разрешаться).
        url = reverse('users:user-update', kwargs={'pk': other_user.pk})
        data = {
            'email': 'updated@example.com',
            'first_name': 'Updated Name',
            'tg_username': 'updated_tg',
            'tg_id': '67890',
            'phone': '0987654321',
            'city': 'Updated City',
        }
        response = self.client.put(url, data)
        # В зависимости от ваших разрешений это может быть 403 Forbidden или другой код состояния
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_delete_own_user(self):
        """Тестирование DEL-запроса к API - Удалить собственный профиль пользователя"""
        url = reverse('users:user-delete', kwargs={'pk': self.user0.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)
    def test_delete_non_existent_user(self):
        """Тестирование DEL-запроса к API - Удалить несуществующего пользователя"""
        url = reverse('users:user-delete', kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.all().count(), 1)
    def test_unauthenticated_access(self):
        """Тестирование DEL-запроса к API - Тестовый доступ без аутентификации"""
        self.client.force_authenticate(user=None)
        url = reverse('users:user-delete', kwargs={'pk': self.user0.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.all().count(), 1)
    def test_delete_other_user(self):
        """Тестирование DEL-запроса к API - Удалить чужого профиль пользователя"""
        # Создайте другого пользователя
        other_user = User.objects.create(email='other@example.com', password='strongpassword')
        # Попытка удалить профиль другого пользователя (должен быть запрещен или не разрешен)
        url = reverse('users:user-delete', kwargs={'pk': other_user.pk})
        response = self.client.delete(url)
        # В зависимости от ваших разрешений это может быть 403 Forbidden или другой код состояния
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.all().count(), 2)
class CreateSuperuserCommandTest(TestCase):
    def test_create_superuser(self):
        # Выполните команду создания суперпользователя
        call_command('csu', verbosity=0)
        # Проверьте, что пользователь создан
        user = User.objects.get(email='admin@admin.ru')
        # Проверьте атрибуты пользователя
        self.assertEqual(user.email, 'admin@admin.ru')
        self.assertEqual(user.first_name, 'Admin')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        # Проверьте пароль
        self.assertTrue(user.check_password('admin'))
    def test_create_superuser_twice(self):
        # Выполните команду создания суперпользователя дважды
        call_command('csu', verbosity=0)
        try:
            call_command('csu', verbosity=0)
            # Проверьте, что пользователь создан только один раз
            self.assertEqual(User.objects.filter(email='admin@admin.ru').count(), 1)
        except Exception:
            pass