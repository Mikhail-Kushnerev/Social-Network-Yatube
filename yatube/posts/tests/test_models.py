from django.test import TestCase

from posts.models import Post, Group, User


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
            text='Тестовая группа',
        )

    def test_title_group(self):
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(
            expected_object_name,
            str(group),
            'title группы не сохранился')

    def test_text_post(self):
        post = PostModelTest.post
        expected_object_name = post.text
        self.assertEqual(expected_object_name, str(post), 'проблемы с текстом')
