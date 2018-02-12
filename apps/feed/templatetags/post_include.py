from django import template


register = template.Library()

@register.inclusion_tag('posts/post.html')
def post_include(post, user):
    return {'post': post, 'user':user}