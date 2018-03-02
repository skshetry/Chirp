from django.conf.urls import url

from .views import get_media, like_post, post_detail, posts_add, share_post

urlpatterns = [
    url(r'^add/', posts_add, name='add'),
    url(r'^(?P<post_id>[0-9a-f-]+)/like', like_post, name='like'),
    url(r'^(?P<post_id>[0-9a-f-]+)/share', share_post, name='share'),
    url(r'^api/(?P<post_id>[0-9a-f-]+)', post_detail, name='post_detail'),
    url(r'^api/media/(?P<media_id>[0-9]+)/', get_media, name='get_media'),
]
