# Generated by Django 2.2.16 on 2022-02-04 12:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0016_auto_20220204_0329'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pro',
            new_name='Profile',
        ),
    ]