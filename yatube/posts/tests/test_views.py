from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.conf import settings
from django.core.cache import cache

from posts.models import Post, Group, User, Follow


class PostPagesViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.author_client = Client()
        cls.author_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='веселье на уровне',
            slug='test-slug',
        )
        for _ in range(settings.POSTS_SITE + settings.PAGE_SITE):
            cls.post = Post.objects.create(
                author=cls.user,
                text='текст',
                group=cls.group,
            )

        cls.user_2 = User.objects.create_user(username='not_follower')
        cls.not_foll = Client()
        cls.not_foll.force_login(cls.user_2)

        cls.follower = User.objects.create_user(username='follower')
        cls.follower_client = Client()
        cls.follower_client.force_login(cls.follower)

        cls.fol_date = Follow.objects.create(
            user=cls.follower,
            author=cls.post.author
        )
        cls.follower_count = Follow.objects.count()

    def test_cache(self):
        cache.clear()
        response = self.client.get(reverse('posts:index'))
        page_obj = response.content
        post_db = Post.objects.all()
        post_db.delete()
        response_2 = self.client.get(reverse('posts:index'))
        page_obj_two = response_2.content
        self.assertEqual(page_obj, page_obj_two)
        cache.clear()
        response_2 = self.client.get(reverse('posts:index')).content
        self.assertNotEqual(page_obj, response_2)

    def test_post_page_show_correct_context(self):

        urls = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug}),
            reverse('posts:profile', kwargs={
                'username': self.user.username}),
            reverse('posts:post_detail', kwargs={
                'post_id': self.post.id})
        ]

        for url in urls:
            response = self.client.get(url)
            if url == urls[-1]:
                site_obj = response.context['text_post']
            else:
                site_obj = response.context['page_obj'][0]
        post_id_0 = site_obj.id
        if post_id_0 == self.post.id:
            post_text_0 = site_obj.text
            post_image_0 = site_obj.image
            post_group_0 = site_obj.group.title
            post_author_0 = site_obj.author.username
            self.assertEqual(post_id_0, self.post.id)
            self.assertEqual(post_text_0, self.post.text)
            self.assertEqual(post_image_0, self.post.image)
            self.assertEqual(post_group_0, self.group.title)
            self.assertEqual(post_author_0, self.user.username)

    def test_create_and_edit_page_show_correct_context_(self):
        """Шаблон home сформирован с правильным контекстом."""
        urls = [
            reverse('posts:create'),
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        ]

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for url in urls:
            response = self.author_client.get(url)
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context.get('form').fields[value]
                    self.assertIsInstance(form_field, expected)

    def test_first_page_contains_ten_records(self):
        templates = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user.username})
        ]
        for template in templates:
            cache.clear()
            response = self.client.get(template)
            self.assertEqual(
                len(response.context['page_obj']), settings.PAGE_SITE
            )

    def test_second_page_contains_three_records(self):
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(
            len(response.context['page_obj']), settings.POSTS_SITE
        )

    def test_new_post_for_followers(self):

        response_not = self.not_foll.get(
            reverse('posts:follow_index')
        )
        self.assertNotIn(self.post, response_not.context['page_obj'])

        response = self.follower_client.get(
            reverse('posts:follow_index')
        )
        self.assertIn(self.post, response.context['page_obj'])

    def test_following(self):

        self.assertTrue(self.follower_count, len(Follow.objects.all()))
        self.not_foll.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': self.user.username}
            ),
            follow=True
        )
        self.assertEqual(len(Follow.objects.all()), self.follower_count + 1)
        self.assertTrue(
            Follow.objects.filter(
                user=self.user_2,
                author=self.post.author
            ).exists()
        )

    def test_following_delete(self):

        self.assertTrue(self.follower_count, len(Follow.objects.all()))
        self.follower_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': self.user.username}
            ),
            follow=True
        )
        self.assertEqual(len(Follow.objects.all()), self.follower_count - 1)
        self.assertFalse(
            Follow.objects.filter(
                user=self.user_2,
                author=self.post.author
            ).exists())
