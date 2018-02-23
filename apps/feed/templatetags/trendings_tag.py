from django import template

from posts.models import Tag


register = template.Library()

@register.simple_tag
def trendings_tag():
    return Tag.objects.all().order_by('-created').order_by('-count')[:10]
