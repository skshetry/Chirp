from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.shortcuts import reverse
from django.urls import reverse_lazy
from .views import user_profile


urlpatterns = [
    url(r'^$', user_profile, name='user_profile'),
    ]