# Generated by Django 2.2.16 on 2022-02-03 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220203_2207'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
