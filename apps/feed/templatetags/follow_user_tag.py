from django import template

from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def follow_user_tag():
    return User.objects.all().order_by('-date_joined')[:10]
