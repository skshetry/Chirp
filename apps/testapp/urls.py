from django.conf.urls import url
from .views import test_view, upload_view, TestView

urlpatterns=[
    url(r'^$', test_view, name='Home'),
    url(r'home2/$', upload_view, name='upload_pic'),
    url(r'test/$', TestView.as_view()),

]
