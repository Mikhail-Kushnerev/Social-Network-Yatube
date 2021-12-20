import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.conf import settings
from django.urls import reverse

from posts.forms import PostForm, CommentForm
from posts.models import Group, User, Post, Comment

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CreateFormTests(TestCase):
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
            text='Текст',
            group=cls.group
        )
        cls.form = PostForm()
        cls.form_comment = CommentForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_add_create_image_post_login(self):
        """Валидная форма создает запись в Post."""

        tasks_count = Post.objects.count()

        urls = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug}),
            reverse('posts:profile', kwargs={
                'username': self.user.username}),
            reverse('posts:post_detail', kwargs={
                'post_id': self.post.id})
        ]

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_create_data = {
            'group': self.group.id,
            'text': 'Тестовый текст',
            'image': uploaded,
        }
        response = self.author_client.post(
            reverse('posts:create'),
            form_create_data,
            follow=True
        )
        element = Post.objects.order_by('-id')[0]
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user.username}))
        self.assertEqual(
            element.text,
            form_create_data['text']
        )
        self.assertEqual(
            element.group.id,
            form_create_data['group']
        )
        self.assertEqual(Post.objects.count(), tasks_count + 1)
        self.assertEqual(element.image, f"posts/{form_create_data['image']}")

        for url in urls:
            response = self.client.get(url)
            if url == urls[-1]:
                site_obj = response.context['text_post']
            else:
                site_obj = response.context['page_obj'][0]
        post_id_0 = element.id
        if post_id_0 == self.post.id:
            post_image_0 = site_obj.image
            self.assertEqual(
                post_image_0,
                f"posts/{form_create_data['image']}"
        )

    def test_edit_post_login(self):
        form_edit_data = {
            'text': 'Изм. текст',
        }
        self.author_client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}),
            form_edit_data
        )
        response = self.client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            )
        )
        info_post = response.context['text_post']
        edit_text = info_post.text
        self.assertEqual(edit_text, form_edit_data['text'])

    def test_comment_post_login(self):
        form_comment_data = {
            'text': 'Коммент от логина',
        }
        self.author_client.post(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}),
            form_comment_data
        )
        response = self.client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            )
        )
        site_obj = response.context['text_post']
        post_comment_0 = site_obj.comments
        self.assertEqual(post_comment_0, self.post.comments)

    def test_create_post_anon(self):
        tasks_count = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст',
        }
        self.client.post(
            reverse('posts:create'), form_data, follow=True)
        self.assertEqual(Post.objects.count(), tasks_count)

    def test_create_comment_anon(self):
        tasks_count = Comment.objects.count()
        form_data_comment = {
            'text': 'Комментарий',
        }
        self.client.post(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            ),
            form_data_comment,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), tasks_count)

    def test_edit_post_anon(self):
        form_edit_data = {
            'text': 'Изм. текст',
        }
        self.client.post(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}),
            form_edit_data
        )
        response = self.client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            )
        )
        info_post = response.context['text_post']
        edit_text = info_post.text
        self.assertEqual(edit_text, self.post.text)
