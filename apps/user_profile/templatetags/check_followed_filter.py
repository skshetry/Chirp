from django import template

from django.contrib.auth.models import User

from posts.models import Post


register = template.Library()

@register.filter(name='check_followed_user_already')
def check_followed_user_already(user, user2):
    return user.user_details.follows.filter(user=user2).exists()
