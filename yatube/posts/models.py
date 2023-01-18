from django.db import models
from django.contrib.auth import get_user_model

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

    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts'
    )

    def __str__(self):
        """Выводим текст поста"""
        return self.text

    class Meta:
        """Сортировка по дате публикации"""
        ordering = ['-pub_date']

