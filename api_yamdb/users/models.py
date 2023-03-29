from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
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
    first_name = models.TextField(
        max_length=150,
        blank=True
    )
    last_name = models.TextField(
        max_length=150,
        blank=True
    )
    """ email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=250,
        unique=True,
    ) """
    role = models.CharField(
        verbose_name='Статус',
        max_length=50,
        choices=ROLES,
        default=USER
    )
