from django.test import TestCase, Client

from http import HTTPStatus


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()

    def test_static_page_url(self) -> None:
        """Страница доступка по URL."""
        pages: tuple = (
            '/about/author/',
            '/about/tech/',
        )
        for page in pages:
            response = self.guest_client.get(page)
            error_name: str = f'Ошибка: нет доступа до страницы {page}'
            self.assertEqual(response.status_code, HTTPStatus.OK, error_name)
