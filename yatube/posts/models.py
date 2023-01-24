from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Group(models.Model):
    """Модель для сообщества."""

    title = models.CharField(max_length=200, verbose_name='Группа')
    slug = models.SlugField(
        max_length=255,
        verbose_name='URL',
        unique=True
    )
    description = models.TextField()

    def __str__(self):
        """Получить имя группы."""
        return self.title


class Post(models.Model):
    """Модель для записей."""

    text = models.TextField(
        'Текст поста',
        help_text='Введите текст поста',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Группа',
    )

    class Meta:
        """Сортировка по дате публикации"""
        ordering = ['-pub_date']

    def __str__(self):
        """Выводим текст поста"""
        return self.text[:15]
