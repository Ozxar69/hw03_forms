from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Post, Group

User = get_user_model()


class PostForm(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Phantomas')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='Test group',
            slug='test-group',
            description='Test group description'
        )

    def test_create_post_form(self):
        """Проверка формы создания поста"""
        count = Post.objects.count()
        form_data = {
            "group": self.group.id,
            'text': 'Test text',
        }
        response = self.authorized_client.post(reverse('posts:post_create'),
                                               data=form_data,
                                               follow=True,
                                               )
        error1 = 'Данные поста не совпадают'
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Post.objects.filter(text='Test text',
                                            group=self.group.id,
                                            author=self.user,).exists(), error1)
        error2 = 'Пост не добавлен в БД'
        self.assertEqual(Post.objects.count(), count + 1, error2)

    def test_edit_post_form(self):
        """Проверка формы редактирования поста"""
        self.post = Post.objects.create(
            text='Test text',
            author=self.user,
            group=self.group,
        )
        original_post = self.post
        self.group2 = Group.objects.create(
            title='Test group2',
            slug='test-group2',
            description='Test group2 description'
        )
        form_data = {
            'text': 'Test text2',
            "group": self.group2.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': original_post.id}),
            data=form_data,
            follow=True,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        error1 = 'Данные поста не совпадают'
        self.assertTrue(Post.objects.filter(
            group=self.group2.id,
            author=self.user,
            pub_date=self.post.pub_date,
        ).exists(), error1)
        error2 = 'Пользователь не может изменить пост'
        self.assertNotEqual(original_post.text, form_data['text'], error2)
        error3 = 'Пользователь не может изменить группу'
        self.assertNotEqual(original_post.group, form_data['group'], error3)
