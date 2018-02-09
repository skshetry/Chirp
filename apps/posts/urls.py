from django.conf.urls import url

from .views import posts_add

urlpatterns = [
    url(r'^add/', posts_add, name='add'),
]