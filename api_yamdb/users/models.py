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
        constraints = [
            models.UniqueConstraint(fields=('username', 'email'),
                                    name='unique_username&email')
        ]

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
