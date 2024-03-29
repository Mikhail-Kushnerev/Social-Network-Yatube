from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.cache import cache_page

from .utils import get_page_context
from .models import User, Post, Group, Follow
from .forms import PostForm, CommentForm
#from users.models import Profile


# @cache_page(20)
def index(request):
    """
    Функция, возвращающая всем пользователям 10 постов на 1 странице
    по убыванию даты создания самих постов.
    """
    template = 'posts/index.html'
    form = CommentForm
    context = {'form': form}
    context.update(
        get_page_context(
            Post.objects.all(),
            request
        )
    )
    return render(
        request,
        template,
        context
    )


def group_posts(request, slug):
    """
    Функция, возвращающая всем пользователям 10 постов на 1 странице
    конкретной группы.
    """
    template = 'posts/group_list.html'
    group = get_object_or_404(
        Group,
        slug=slug
    )
    title = f'Записи сообщества {group}'
    description = group.description
    # posts = group.group_post.all()
    context = {
        # 'posts': posts,
        'group': group,
        'title': title,
        'description': description,
    }
    context.update(
        get_page_context(
            group.group_post.all(),
            request
        )
    )
    return render(
        request,
        template,
        context
    )


def profile(request, username):
    """
    Функция, возвращающая всем пользователям 10 постов на 1 странице
    определенного автора.
    """
    template = 'posts/profile.html'
    user = request.user
    author = get_object_or_404(
        User,
        username=username
    )
    # posts = author.posts.all()
    following = Follow.objects.filter(
        user__username=user,
        author=author
    ).exists()
    context = {
        # 'posts': posts,
        'author': author,
        'following': following,
    }
    context.update(
        get_page_context(
            author.posts.all(),
            request
        )
    )
    return render(
        request,
        template,
        context
    )


def profile_page(request, username):
    template = 'posts/profile_page.html'
    post_count = Post.objects.all()
    follow = Follow.objects.filter(
        user=request.user,
    )
    # pp = Pro.objects.filter(user=follow[0].author)[0]
    context = {
        'post_count': post_count,
        'follow': follow,
        # 'pp': pp
    }
    #us = User.objects.filter(username=request.user.username)
    return render(request, template, context)


def post_detail(request, post_id):
    """
    Функция, возвращающая всем пользователям подробную информацию
    об конкретном посте:
    - дата создания;
    - группу поста;
    - текст поста;
    - картинку поста;
    - имя автора.
    Есть возможность комментировать данный пост.
    """
    template = 'posts/post_detail.html'
    post = get_object_or_404(
        Post,
        pk=post_id
    )
    form = CommentForm()
    comments = post.comments.all()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(
        request,
        template,
        context
    )


@login_required
def post_create(request):
    """
    Функция, возвращающая зарегестрированным пользователям
    форму для создания поста.
    """
    template = 'posts/create_post.html'
    title = "Новый пост"
    text = "Добавление поста"
    apply = "Создать пост"
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        post = form.save(False)
        post.author = request.user
        post.save()
        return redirect(
            'posts:profile',
            username=post.author
        )
    return render(
        request,
        template,
        {
            'form': form,
            'title': title,
            'text': text,
            'apply': apply,
        }
    )


@login_required
def post_edit(request, post_id):
    """
    Функция, возвращающая автору поста пользователям форму
    для редактирования поста.
    """
    post = get_object_or_404(
        Post,
        pk=post_id
    )
    if post.author != request.user:
        return redirect(
            'posts:post_detail',
            post_id
        )
    title = "Редактировать запись"
    text = "Редактирование поста"
    apply = "Сохранить изменения"
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        post = form.save()
        return redirect(
            'posts:post_detail',
            post_id
        )
    return render(
        request,
        "posts/create_post.html",
        {
            'form': form,
            'post': post,
            'title': title,
            'text': text,
            'apply': apply,
        }
    )


@login_required
def add_comment(request, post_id):
    """
    Функция, возвращающая зарегестрированным пользователям форму для
    комментирования кокретного поста.
    """
    post = get_object_or_404(
        Post,
        pk=post_id
    )
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect(
        'posts:post_detail',
        post_id=post_id
    )


@login_required
def follow_index(request):
    """
    Функция, возвращающая 10 постов от избранных авторов на 1 странице
    по дате создания самих постов.
    """
    post_list = Post.objects.filter(author__following__user=request.user)
    context = {}
    context.update(
        get_page_context(
            post_list,
            request
        )
    )
    return render(
        request,
        "posts/follow.html",
        context
    )


@login_required
def profile_follow(request, username):
    """
    Функция, возвращающая возможнсоть зарегестрированным пользователям
    подписаться на конкретного автора.
    """
    author = get_object_or_404(
        User,
        username=username
    )
    try:
        Follow.objects.get_or_create(
            user=request.user,
            author=author
        )
    except IntegrityError:
        pass
    return redirect(
        'posts:profile',
        username=username
    )


@login_required
def profile_unfollow(request, username):
    """
    Функция, возвращающая возможнсоть зарегестрированным пользователям
    отписаться от конкретного автора.
    """
    author = get_object_or_404(
        User,
        username=username
    )
    profile_follow = get_object_or_404(
        Follow,
        author=author,
        user=request.user
    )
    if Follow.objects.filter(pk=profile_follow.pk).exists():
        profile_follow.delete()
    return redirect(
        'posts:profile',
        username=username
    )
