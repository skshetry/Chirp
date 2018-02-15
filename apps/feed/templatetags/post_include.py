from django import template

from posts.models import Post

register = template.Library()

@register.inclusion_tag('posts/post.html')
def post_include(post, user):
    return {'post': post, 'user':user}

@register.simple_tag
def posts_from_feed(user):
    return Post.objects.filter(feed__user=user).select_related('user').order_by('-created')

@register.simple_tag
def media_posts(post):
    return post.get_medias()
