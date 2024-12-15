from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Ваш E-mail')
    first_name = models.CharField(max_length=50, verbose_name='Ваше имя', **NULLABLE)
    tg_username = models.CharField(max_length=50, verbose_name='Ваш Telegram_name', **NULLABLE)
    tg_id = models.CharField(max_length=20, verbose_name='Ваш Telegram_id', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватарка', **NULLABLE)
    is_subscribe = models.BooleanField(default=False, verbose_name='Подписка на напоминания', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'
