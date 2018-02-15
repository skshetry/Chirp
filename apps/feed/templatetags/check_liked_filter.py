from django import template

from django.contrib.auth.models import User

from posts.models import Post


register = template.Library()

@register.filter(name='check_liked_posts')
def check_liked_posts(post, user):
    user_id = int(user.id)
    return post.likes.filter(id=user_id).exists()

@register.filter(name='check_shared_posts')
def check_shared_posts(post, user):
    user_id = int(user.id)
    return Post.objects.filter(shared_post=post).filter(user=user).exists()
