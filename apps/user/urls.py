from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.shortcuts import reverse
from .views import settings_view


urlpatterns = [
    url(r'^settings/$', settings_view, name='settings'),
    url(r'^settings/change-password/$', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='done'), name='change_password'),
    url(r'^settings/change-password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='password_change_done'),
]