from django import template

register = template.Library()

@register.filter(name='check_followed_user_already')
def check_followed_user_already(user, user2):
    return user.user_details.follows.filter(user=user2).exists()
