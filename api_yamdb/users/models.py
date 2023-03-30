from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=250,
        unique=True,
    )
    first_name = models.TextField(
        max_length=150,
        blank=True
    )
    last_name = models.TextField(
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Статус пользователя',
        max_length=50,
        choices=ROLES,
        default=USER
    )


class Meta:
    ordering = ('username',)

    def __str__(self):
        return self.username
