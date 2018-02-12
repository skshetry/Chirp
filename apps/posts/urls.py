from django.conf.urls import url

from .views import posts_add, like_post

urlpatterns = [
    url(r'^add/', posts_add, name='add'),
    url(r'^(?P<post_id>[0-9a-f-]+)/like', like_post, name='like'),
]