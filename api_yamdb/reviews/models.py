from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from titles.models import Title


class Review(models.Model):
    """Модель для отзыва."""
    text = models.TextField(verbose_name='Текст отзыва')
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(
                limit_value=1, message='Оценка не может быть меньше 1'
            ),
            MaxValueValidator(
                limit_value=10, message='Оценка не может быть больше 10'
            )]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(fields=('author', 'title'),
                                    name='unique_author_title'),
        )

    def __str__(self):
        return f'Произведение: {str(self.title)[:15]}, Автор: {self.author}'


class Comment(models.Model):
    """Модель для комментария к отзыву."""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата добавления'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:15]
