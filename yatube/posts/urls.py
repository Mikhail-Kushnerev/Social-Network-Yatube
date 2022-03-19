from django.urls import path, re_path

from . import views
# from users.views import picture

app_name = 'posts'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path(
        'group/<slug:slug>/',
        views.group_posts,
        name='group_list'
    ),
    re_path(
        r'profile/(?P<username>[\w.@+-]+)/$',
        views.profile,
        name='profile'
    ),
    re_path(
        r'profile_page/(?P<username>[\w.@+-]+)/$',
        views.profile_page,
        name='profile_page'
    ),
    # path('profile_page/<str:username>/', picture, name='profile_page'),
    re_path(
        r'posts/(?P<post_id>\d+)/$',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'create/',
        views.post_create,
        name='create'
    ),
    re_path(
        r'posts/(?P<post_id>\d+)/edit/$',
        views.post_edit,
        name='post_edit'
    ),
    re_path(
        r'posts/(?P<post_id>\d+)/comment/$',
        views.add_comment,
        name='add_comment'
    ),
    path(
        'follow/',
        views.follow_index,
        name='follow_index'
    ),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name="profile_unfollow"
    ),
]
