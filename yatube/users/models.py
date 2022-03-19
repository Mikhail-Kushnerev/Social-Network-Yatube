from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        null=True,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        default='default.jpg',
        null=True,
        blank=True,
        upload_to='images/profile/'
    )

    def __str__(self):
        return f'Profile {self.user.username}'
