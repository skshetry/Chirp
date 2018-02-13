from django import template

from django.contrib.auth.models import User

from posts.models import Post


register = template.Library()

@register.filter(name='check_liked_posts')
def check_liked_posts(post, user):
    user_id = int(user.id)
    return post.likes.filter(id=user_id).exists()
