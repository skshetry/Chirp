from django.conf.urls import url

from .views import follow_user, profile_photo, user_profile

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', user_profile, name='user_profile'),
    url(r'^(?P<username>[\w.@+-]+)/follow$', follow_user, name='follow_user'),
    url(r'^(?P<username>[\w.@+-]+)/profile_photo$',
        profile_photo, name="profile_photo"),
]
