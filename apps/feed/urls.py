from django.conf.urls import url

from .views import HomeView, retrieve_new_post, get_feed_lists, get_recent_after, get_posts_before

urlpatterns = [
    url(r'^new-feed/(?P<post_id>[0-9a-f-]+)',
        retrieve_new_post, name="new_posts_retrieve_ajax"),
    url(r'^get-feed-list/', get_feed_lists, name='get_feed_list_ajax'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^get-recent-after/(?P<post_id>[0-9a-f-]+)', get_recent_after, name='get_recent_posts_ajax'),
    url(r'^get-posts-before/(?P<post_id>[0-9a-f-]+)', get_posts_before, name='get_posts_before_ajax'),

]
