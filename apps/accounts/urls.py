from django.conf.urls import url
from .views import UserLoginView, logout_view, signup


urlpatterns = [
    url(r'signup/$', signup, name='signup'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
]
