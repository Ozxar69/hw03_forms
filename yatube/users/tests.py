from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from http import HTTPStatus

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Phantomas')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_guest_access_pages(self) -> None:
        """Страница доступка по URL."""
        pages: tuple = (
            '/auth/signup/',
            '/auth/login/',
            '/auth/users/password_reset/',
        )
        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_users_access_pages(self) -> None:
        """Страница доступка по URL."""
        pages: tuple = (
            '/auth/password_change/',
            '/auth/logout/',
        )
        for page in pages:
            response = self.authorized_client.get(page)
            error_name: str = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)

    def test_guest_access_pages_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
            '/auth/users/password_reset/': 'users/password_reset_form.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                error_name: str = f'Ошибка: {address} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)

    def test_users_access_pages_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        self.authorized_client.force_login(self.user)
        templates_url_names = {
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/logout/': 'users/logged_out.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                error_name: str = f'Ошибка: {address} ожидал шаблон {template}'
                self.assertTemplateUsed(response, template, error_name)
