from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings
from django import forms

from ..models import Post, Group

User = get_user_model()


class PostModelTest(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Phantomas')
        self.user2 = User.objects.create_user(username='Commissioner')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(title='Тестовая группа',
                                          slug='test_group')
        self.post = Post.objects.create(text='Тестовый текст',
                                        group=self.group,
                                        author=self.user)

    def test_views_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse('posts:main_paige'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug':
                            f'{self.group.slug}'}): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username':
                            f'{self.user.username}'}): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={'post_id':
                            self.post.id}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={'post_id':
                            self.post.id}): 'posts/create_post.html'}
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name = f'Ошибка: {adress} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)

    def test_views_correct_context(self):
        """Контекст использует соответствующий шаблон."""
        templates_context_names = {
            reverse('posts:main_paige'): {
                'group': self.group,
        }
        }
        for adress, context in templates_context_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                error_name = f'Ошибка: {adress} ожидал контекст {context}'
                self.assertTemplateUsed(response, 'posts/index.html', error_name)