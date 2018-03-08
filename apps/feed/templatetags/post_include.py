from django import template
from django.db.models import (BooleanField, Case, Count, IntegerField, Value,
                              When)

from posts.models import Post

register = template.Library()


@register.inclusion_tag('posts/post.html')
def post_include(post, user):
    return {'post': post, 'user': user}


def get_all_posts():
    return Post.objects.prefetch_related(
        'posts_media'
    ).prefetch_related(
        'user__user_details'
    ).prefetch_related(
        'shared_post'
    ).prefetch_related(
        'shared_post__user'
    ).prefetch_related(
        'shared_post__posts_media'
    ).prefetch_related(
        'shared_post__user__user_details'
    ).prefetch_related(
        'parent'
    ).prefetch_related(
        'parent__user'
    ).prefetch_related(
        'parent__posts_media'
    ).prefetch_related(
        'parent__user__user_details'
    ).prefetch_related(
        'post_childs'
    ).prefetch_related(
        'post_childs__user'
    ).prefetch_related(
        'post_childs__posts_media'
    ).prefetch_related(
        'post_childs__user__user_details'
    ).prefetch_related(
        'likes'
    )


@register.simple_tag
def posts_from_feed(user):
    return get_all_posts().filter(
        feed__user=user
    ).annotate(
        post_liked=Case(
            When(likes=user, then=True),
            default=Value(False),
            output_field=BooleanField(),
        )).annotate(
        shared=Case(
            When(post_shared__user=user, then=True),
            When(shared_post__user=user, then=True),
            When(shared_post__post_shared__user=user, then=True),
            default=Value(False),
            output_field=BooleanField(),
        )).annotate(
        shared_count=Case(
            When(shared_post__isnull=True, then=Count('post_shared')),
            default=Count('shared_post', distinct=True),
            output_field=IntegerField(),
        )).order_by('-created')[:200]


@register.simple_tag
def media_posts(post):
    return post.get_medias()


@register.simple_tag
def posts_from_users_profile(user, viewer=None):
    if viewer is None:
        viewer = user
    return get_all_posts().filter(
        user=user
    ).annotate(
        post_liked=Case(
            When(likes=viewer, then=True),
            default=Value(False),
            output_field=BooleanField(),
        )).annotate(
        shared=Case(
            When(post_shared__user=viewer, then=True),
            When(shared_post__user=viewer, then=True),
            When(shared_post__post_shared__user=viewer, then=True),
            default=Value(False),
            output_field=BooleanField(),
        )).annotate(
        shared_count=Case(
            When(shared_post__isnull=False, then=Count('shared_post__post_shared')),
            default=Count('shared_post'),
            output_field=IntegerField(),
        )).order_by('-created')[:200]
