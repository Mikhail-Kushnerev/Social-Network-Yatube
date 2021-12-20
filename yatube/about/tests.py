from django.test import TestCase, Client
from http import HTTPStatus


class StaticPagesURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованый клиент
        self.guest_client = Client()

    def test_templates(self):
        templates_names = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
        }
        for template, adress in templates_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_url(self):
        url_names = {
            'author': '/about/author/',
            'tech': '/about/tech/',
        }
        for field, url in url_names.items():
            with self.subTest(field=field):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
