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
        self.assertEqual(
            element.image,
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
                'posts:add_comment',
                kwargs={'post_id': self.post.id}
            ),
            form_comment_data,
            follow=True
        )
        comment_post = Comment.objects.order_by('-created')[0]
        self.client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            )
        )
        self.assertEqual(comment_post.text, form_comment_data['text'])
        self.assertEqual(comment_post.id, self.post.id)

    def test_create_post_anon(self):
        post_count = Post.objects.count()
        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст',
        }
        self.client.post(
            reverse('posts:create'), form_data, follow=True)
        self.assertEqual(Post.objects.count(), post_count)

    def test_create_comment_anon(self):
        comment_count = Comment.objects.count()
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
        self.assertEqual(Comment.objects.count(), comment_count)

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
