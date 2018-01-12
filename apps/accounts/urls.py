from django.conf.urls import url
from .views import UserLoginView, logout_view, signup, activate as activate_view 


urlpatterns = [
    url(r'signup/$', signup, name='signup'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate_view, name='activate'),

]
