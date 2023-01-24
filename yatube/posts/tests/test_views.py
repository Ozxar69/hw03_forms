User = get_user_model()


class PostModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Some group',  # Создаем группу для тестов 1 раз
            slug='some-group',
            description='Тестовая группа'
        )

    def setUp(self):
        self.user = User.objects.create_user(username='registered')  # Создаем пользователя для каждого теста
        self.authorized_client = Client()  # Создаем клиент (своего рода браузер)
        self.authorized_client.force_login(self.user)  # Авторизуем пользователя

    def test_post_create_auth(self):
        response = self.authorized_client.post(
            reverse('new_post'),
            data={'text': 'Nice post', 'group': PostModelTest.group.id},
            follow=True,
        )  # Отправляем данные для создания нового поста на адрес new_post (или как он у вас называется)
        self.assertEqual(response.status_code, 200)  # Убеждаемся, что УРЛ отработал корректно 
        self.assertEqual(Post.objects.count(), 1)  # Убеждаемся, что в БД появился 1 пост
        post = Post.objects.first()  # Достаем пост из БД 
        self.assertEqual(post.text, 'Nice post')  # Убеждаемся, текст поста совпадает с тем, что мы передали 
        self.assertEqual(post.author, self.user)  # Убеждаемся, что у поста нужный автор
        self.assertEqual(post.group.slug, PostModelTest.group.slug)  # Сравниваем, например, равенство слагов