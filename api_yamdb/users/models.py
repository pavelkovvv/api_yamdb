from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


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
        max_length=254,
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
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=150,
        null=True,
        default=None
    )

    class Meta:
        ordering = ('username',)
        unique_together = ('username', 'email')

        def __str__(self):
            return self.username

    @property
    def is_user(self):
        if self.role == self.USER:
            return True
        else:
            return False

    @property
    def is_moderator(self):
        if self.role == self.MODERATOR:
            return True
        else:
            return False

    @property
    def is_admin(self):
        if self.role == self.ADMIN:
            return True
        else:
            return False


User = get_user_model()
