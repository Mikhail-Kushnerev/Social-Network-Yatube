from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedModel

User = get_user_model()


class Post(models.Model):

    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name='group_post',
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Выберите группу'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date', )

    def __str__(self):
        return self.text[:15]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Добавьте комментарий к посту'
    )


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='Группа')
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    def __str__(self):
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )
