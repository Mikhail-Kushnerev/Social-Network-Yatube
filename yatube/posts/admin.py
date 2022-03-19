from django.contrib import admin

from .models import Comment, Post, Group, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'trim50',
        'created',
        'author',
        'group',
        'image',
    )
    search_fields = ('text',)
    list_filter = ('author', 'created')
    list_editable = ('group',)
    empty_value_display = '-пусто-'
    list_per_page = 10


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'post',
        'author',
        'text',
        'created',
    )
    search_fields = ('text',)
    list_filter = ('author', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )


admin.site.register(Group)
