from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import logout_view, UserLoginView


urlpatterns = [
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),

]