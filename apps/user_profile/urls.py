from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.shortcuts import reverse
from django.urls import reverse_lazy
from .views import user_profile, photo_list


urlpatterns = [
    url(r'^$', user_profile, name='user_profile'),
    url(r'^photo$', photo_list, name='photo_list'),
    ]