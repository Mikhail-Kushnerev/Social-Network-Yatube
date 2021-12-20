from django.test import TestCase, Client
from http import HTTPStatus

from posts.models import Group, Post, User


class PostPagesURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.author_client = Client()
        cls.author_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа',
            group=cls.group
        )

    def test_valid_url_200_response_anon_and_login(self):
        """Статус при переходи на ссылке для ноунейма и залогированного"""

        pathnames_to_test = {
            'group_list': f'/group/{self.group.slug}/',
            'profile': f'/profile/{self.user}/',
            'post_detail': f'/posts/{self.post.id}/',
            'create': f'/{self.user.username}/login/?next=/create/',
        }
        for field, url in pathnames_to_test.items():
            with self.subTest(field=field):
                response_anon = self.client.get(url, follow=True)
                self.assertEqual(response_anon.status_code, HTTPStatus.OK)

    def test_valid_url_200_response_auth(self):
        '''Статус при переходи на ссылке для автора'''

        response = self.author_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_templates_guest(self):
        templates_names = {
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
        }
        for adress, template in templates_names.items():
            with self.subTest(adress=adress):
                response = self.author_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_templates_guest(self):
        templates_names = {
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.user}/',
            'posts/post_detail.html': f'/posts/{self.post.id}/',
        }
        for template, adress in templates_names.items():
            with self.subTest(adress=adress):
                response = self.client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_templates_author(self):
        templates_names = {
            '/create/': 'posts/create_post.html',
            '/follow/': 'posts/follow.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
        }
        for adress, template in templates_names.items():
            with self.subTest(adress=adress):
                response = self.author_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_valid_url_302_response_anon(self):
        pathnames_to_test = {
            'create': '/create/',
            'post_edit': f'/posts/{self.post.id}/edit/',
        }
        for field, url in pathnames_to_test.items():
            with self.subTest(field=field):
                response_anon = self.client.get(url)
                self.assertEqual(response_anon.status_code, HTTPStatus.FOUND)

    def test_error_page(self):
        response = self.client.get('/abcd/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
