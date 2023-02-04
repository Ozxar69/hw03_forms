from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings
from django import forms

from ..models import Post, Group
from ..forms import PostForm

TEST_OF_POSTS: int = 13
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
        self.post = Post.objects.create(text='Тестовый пост',
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

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:main_paige'))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author
        post_text_0 = first_object.text
        post_group_0 = first_object.group
        self.assertEqual(post_author_0, self.user)
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_group_0, self.group)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': f'{self.group.slug}'}))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author
        post_text_0 = first_object.text
        post_group_0 = first_object.group
        self.assertEqual(post_author_0, self.user)
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_group_0, self.group)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': f'{self.user.username}'}))
        first_object = response.context['page_obj'][0]
        form_fields = {
            first_object.text: self.post.text,
            first_object.group: self.group,
            first_object.author: self.user
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))
        post_text_0 = {response.context['posts'].text: self.post.text,
                       response.context['posts'].group: self.group,
                       response.context['posts'].author: self.user.username}
        for value, expected in post_text_0.items():
            self.assertEqual(post_text_0[value], expected)

    def test_create_edit_page_show_correct_form(self):
        """post_create и post_edit сформированы с правильным контекстом."""
        urls = (
            ('posts:post_create', None),
            ('posts:post_edit', (self.post.id,)),
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ChoiceField,
        }
        for url, slug in urls:
            reverse_name = reverse(url, args=slug)
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get('form').fields.get(
                            value
                        )
                        self.assertIsInstance(form_field, expected)
                        self.assertIsInstance(response.context['form'],
                                              PostForm)

    def test_post_added_correctly(self):
        """Пост при создании добавлен корректно"""
        post = Post.objects.create(
            text=self.post.text,
            author=self.user,
            group=self.group)
        response_index = self.authorized_client.get(
            reverse('posts:main_paige')
        )
        response_group = self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': f'{self.group.slug}'})
        )
        response_profile = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': f'{self.user.username}'})
        )
        index = response_index.context['page_obj']
        group = response_group.context['page_obj']
        profile = response_profile.context['page_obj']
        self.assertIn(post, index, 'поста нет на главной')
        self.assertIn(post, group, 'поста нет в профиле')
        self.assertIn(post, profile, 'поста нет в группе')

    def test_post_added_correctly_user2(self):
        """Пост при создании виден в группе, на главной и не добавляется
        другому пользователю"""
        group2 = Group.objects.create(
            title='group2',
            slug='group2',
        )
        posts_count = Post.objects.filter(group=self.group).count()
        post = Post.objects.create(
            text=self.post.text,
            author=self.user2,
            group=group2
        )
        response_profile = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': f'{self.user.username}'})
        )
        group = Post.objects.filter(group=self.group).count()
        profile = response_profile.context['page_obj']
        self.assertEqual(group, posts_count, 'Пост не добавлен в группу')
        self.assertNotIn(post, profile, 'Пост не добавлен в профиль')


class PaginatorViewsTest(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth_phantomas')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='group',
            slug='group',
        )
        bilk_post: list = []
        for i in range(TEST_OF_POSTS):
            bilk_post.append(
                Post(
                    text=f'post {i}',
                    author=self.user,
                    group=self.group,
                )
            )
        Post.objects.bulk_create(bilk_post)

    def test_index_page_show_correct_number_of_posts(self):
        """Проверка количества постов на главной странице, в группе и в профиле
        для авторизованного пользователя и не авторизованного."""
        pages: tuple = (
            reverse('posts:main_paige'),
            reverse('posts:group_list', kwargs={'slug': f'{self.group.slug}'}),
            reverse('posts:profile', kwargs={'username': f'{self.user.username}'})
        )
        for page in pages:
            response1 = self.authorized_client.get(page)
            response2 = self.authorized_client.get(page + '?page=2')
            response3 = self.guest_client.get(page)
            response4 = self.guest_client.get(page + '?page=2')
            count_posts1 = len(response1.context['page_obj'])
            count_posts2 = len(response2.context['page_obj'])
            count_posts3 = len(response3.context['page_obj'])
            count_posts4 = len(response4.context['page_obj'])
            error1 = (f'Ошибка: постов - {count_posts1},'
                      f'должно быть {settings.NUMBER_OF_POSTS_ON_PAGE}')
            error2 = (f'Ошибка: постов - {count_posts2},'
                      f'должно быть '
                      f'{TEST_OF_POSTS -settings.NUMBER_OF_POSTS_ON_PAGE}')
            error3 = (f'Ошибка: постов - {count_posts3},'
                      f'должно быть {settings.NUMBER_OF_POSTS_ON_PAGE}')
            error4 = (f'Ошибка: постов - {count_posts4},'
                      f'должно быть'
                      f'{TEST_OF_POSTS -settings.NUMBER_OF_POSTS_ON_PAGE}')
            count2 = TEST_OF_POSTS - settings.NUMBER_OF_POSTS_ON_PAGE
            self.assertEqual(count_posts1, settings.NUMBER_OF_POSTS_ON_PAGE, error1),
            self.assertEqual(count_posts2,
                             count2,
                             error2),
            self.assertEqual(count_posts3, settings.NUMBER_OF_POSTS_ON_PAGE, error3),
            self.assertEqual(count_posts4,
                             count2,
                             error4)
