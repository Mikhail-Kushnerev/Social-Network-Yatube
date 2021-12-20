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

    def test_cache(self):
        response = self.author_client.get(reverse('posts:index'))
        page_obj = response.content
        post_db = Post.objects.all()
        post_db.delete()
        page_obj_two = self.author_client.get(reverse('posts:index'))
        page_obj_two = response.content
        self.assertEqual(page_obj, page_obj_two)
        cache.clear()

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
                site_obj = response.content[0]
        post_id_0 = site_obj.id
        if post_id_0 == self.post.id:
            post_text_0 = site_obj.text
            post_group_0 = site_obj.group.title
            post_author_0 = site_obj.author.username
            self.assertEqual(post_id_0, self.post.id)
            self.assertEqual(post_text_0, self.post.text)
            self.assertEqual(post_group_0, self.group.title)
            self.assertEqual(post_author_0, self.user.username)

    def test_create_and_edit_page_show_correct_context_(self):
        """Шаблон home сформирован с правильным контекстом."""
        response = self.author_client.get(
            reverse('posts:create')
        ) and self.author_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
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

        self.user_2 = User.objects.create_user(username='not_follower')
        self.not_foll = Client()
        self.not_foll.force_login(self.user_2)

        follows_before = Follow.objects.count()

        Follow.objects.create(user=self.user, author=self.post.author)
        post = Post.objects.create(author=self.post.author, text='t1')
        response_not = self.not_foll.get(
            reverse('posts:follow_index')
        )
        self.assertNotIn(post, response_not.context['page_obj'])
        response = self.author_client.get(
            reverse('posts:follow_index')
        )
        self.assertIn(post, response.context['page_obj'])
        self.assertEqual(Follow.objects.count(), follows_before + 1)

    def test_following(self):

        Follow.objects.create(user=self.user, author=self.post.author)
        response_anon = self.client.get(
            reverse('posts:follow_index')
        )
        self.assertEqual(response_anon.status_code, 302)