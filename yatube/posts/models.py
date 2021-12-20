from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):

    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    group = models.ForeignKey(
        'Group',
        on_delete=models.SET_NULL,
        related_name='group_post',
        blank=True,
        null=True
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


class Comment(models.Model):
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
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    title = models.CharField(max_length=200, )
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)

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
