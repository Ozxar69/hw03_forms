from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings
from django import forms

from ..models import Post, Group

User = get_user_model()


class PostModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Some group',
            slug='some-group',
            description='Тестовая группа'
        )

    def setUp(self):
        self.user = User.objects.create_user(username='Phantomas')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # def test_post_create_auth(self):
    #     response = self.authorized_client.post(
    #         reverse('new_post'),
    #         data={'text': 'Nice post', 'group': PostModelTest.group.id},
    #         follow=True,
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(Post.objects.count(), 1)
    #     post = Post.objects.first()
    #     self.assertEqual(post.text, 'Nice post')
    #     self.assertEqual(post.author, self.user)
    #     self.assertEqual(post.group.slug, PostModelTest.group.slug)
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: reverse(name)"
        templates_pages_names = {
            'posts/index.html': reverse('posts:main_paige'),
            'posts/group_posts.html': reverse('posts:group_list',
                                              kwargs={'slug': f'{self.group.slug}'}
                                              ),
            'posts/profile.html': reverse('posts:profile',
                                          kwargs={'username': f'{self.user.username}'}
                                          ),
            'posts/post_detail.html': reverse('posts:post_detail',
                                              kwargs={'post_id': self.post.id}),
            'posts/post_create': reverse('posts:post_create'),
            'posts/post_edit': reverse('posts:post_create',
                                       kwargs={'post_id': self.post.id})
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                error_name = f'Ошибка: {adress} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)
