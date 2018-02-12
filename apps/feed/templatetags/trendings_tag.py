from django import template

from django.contrib.auth.models import User

from posts.models import Tag


register = template.Library()

@register.simple_tag
def trendings_tag():
    return Tag.objects.all().order_by('-created')[:10]
