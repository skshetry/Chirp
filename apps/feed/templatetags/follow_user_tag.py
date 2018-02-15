from django import template

from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def follow_user_tag(user):
    return User.objects.all().exclude(
        user_details__followed_by__user=user,
        ).exclude(
            user_details__user=user,
            ).select_related('user_details').order_by('-date_joined')[:10]
