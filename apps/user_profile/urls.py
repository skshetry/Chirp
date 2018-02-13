from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.shortcuts import reverse
from django.urls import reverse_lazy
from .views import user_profile, follow_user


urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', user_profile, name='user_profile'),
    url(r'^(?P<username>[\w.@+-]+)/follow$', follow_user, name='follow_user'),
    ]