from django.conf.urls import url
from .views import test_view, upload_view

urlpatterns=[
    url(r'^$',test_view),
    url(r'home/$', upload_view, name='upload_pic'),
]