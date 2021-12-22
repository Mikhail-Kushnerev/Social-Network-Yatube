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
        cls.follower = Follow.objects.create(
            user=cls.user,
            author=cls.post.author
        )
        cls.follower_order_id = Follow.objects.order_by('-user_id')[0]

    def test_cache(self):
        cache.clear()
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

        response_not = self.not_foll.get(
            reverse('posts:follow_index')
        )
        self.assertNotIn(self.post, response_not.context['page_obj'])
        response = self.author_client.get(
            reverse('posts:follow_index')
        )
        self.assertIn(self.post, response.context['page_obj'])

    def test_following(self):

        foll_man = self.follower_order_id
        self.assertEqual(foll_man.id, self.follower.id)

    def test_following_delete(self):

        self.follower_order_id.delete()
        Follow.objects.count()
        self.assertEqual(Follow.objects.count(), 0)
