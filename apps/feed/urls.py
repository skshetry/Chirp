from django.conf.urls import url

from .views import HomeView, retrieve_new_post

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^new-feed/(?P<post_id>[0-9a-f-]+)',
        retrieve_new_post, name="new_posts_retrieve_ajax"),
]
