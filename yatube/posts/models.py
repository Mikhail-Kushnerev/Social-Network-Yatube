from django.db import models
from django.contrib.auth.models import User
from django.db.models.expressions import F
from django.db.models.query_utils import Q

from core.models import CreatedModel


class Post(CreatedModel):

    text = models.TextField(
        verbose_name='Текст',
        help_text='Введите текст'
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
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created',)

    def __str__(self):
        return self.text[:15]

    def trim50(self):
        return "%s..." % (self.text[:50],)
    trim50.short_description = "Текст"


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
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Группа'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'),
            models.CheckConstraint(
                check=~Q(user=F('author')), name='dont_follow_yourself'
            )
        ]
        ordering = ["-user"]
        verbose_name = "подписка"
        verbose_name_plural = "подписки"

        def __str__(self):
            return f'{self.user.username} подписался на {self.author.username}'
