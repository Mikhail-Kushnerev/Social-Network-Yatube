from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.cache import cache_page

from .models import User, Post, Group, Follow
from .forms import PostForm, CommentForm


@cache_page(20)
def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(
        posts,
        settings.PAGE_SITE
    )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(
        request,
        template,
        context
    )


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(
        Group,
        slug=slug
    )
    title = f'Записи сообщества {group.title}'
    description = group.description
    posts = group.group_post.all()
    paginator = Paginator(
        posts,
        settings.PAGE_SITE
    )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'title': title,
        'description': description,
        'page_obj': page_obj,
    }
    return render(
        request,
        template,
        context
    )


def profile(request, username):
    template = 'posts/profile.html'
    user = request.user
    author = get_object_or_404(
        User,
        username=username
    )
    posts = author.posts.all()
    paginator = Paginator(
        posts,
        settings.PAGE_SITE
    )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = Follow.objects.filter(user__username=user,
                                      author=author).count()
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following,
    }
    return render(
        request,
        template,
        context
    )


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    text_post = get_object_or_404(
        Post,
        pk=post_id
    )
    form = CommentForm()
    comments = text_post.comments.all()
    context = {
        'text_post': text_post,
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
    post = get_object_or_404(
        Post,
        pk=post_id
    )
    if post.author != request.user:
        return redirect('posts:index')
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
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, settings.PAGE_SITE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "posts/follow.html",
        {'page_obj': page_obj, 'paginator': paginator}
    )


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    profile_follow = Follow.objects.get(author=author,
                                        user=request.user)
    if Follow.objects.filter(pk=profile_follow.pk).exists():
        profile_follow.delete()
    return redirect('posts:profile', username=username)
