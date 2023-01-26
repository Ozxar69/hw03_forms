from django.contrib.auth import get_user_model
from django.test import TestCase
from django.conf import settings

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        error_name = f"Вывод не имеет {settings.NUMBER_OF_SYMBOLS} символов"
        self.assertEqual(self.post.__str__(),
                         self.post.text[:settings.NUMBER_OF_SYMBOLS],
                         error_name)

    def test_models_have_correct_object_title(self):
        """Проверяем group.title."""
        group = PostModelTest.group
        group_title = group.title
        self.assertEqual(group_title, str(group))
