from django import template

from django.db.models import Count
from posts.models import Post


register = template.Library()

@register.inclusion_tag('posts/post.html')
def post_include(post, user):
    return {'post': post, 'user':user}

def get_all_posts():
        return Post.objects.prefetch_related(
        'posts_media'
        ).select_related(
                'user__user_details'
                ).select_related(
                    'shared_post'
                    ).select_related(
                        'shared_post__user'
                        ).select_related(
                            'parent'
                            ).select_related(
                                'parent__user'
                                ).prefetch_related(
                                    'parent__posts_media'
                                    ).select_related(
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
    return get_all_posts().filter(feed__user=user).annotate(shared_count=Count('post_shared')).order_by('-created')


@register.simple_tag
def media_posts(post):
    return post.get_medias()

@register.simple_tag
def posts_from_users_profile(user):
    return get_all_posts().filter(user=user).annotate(shared_count=Count('post_shared')).order_by('-created')

