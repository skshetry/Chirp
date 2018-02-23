from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .views import settings_view

urlpatterns = [
    url(r'^$', settings_view, name='settings'),
    url(r'^change-password/$', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url=reverse_lazy('settings:password_change_done')), name='change_password'),
    url(r'^change-password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='password_change_done'),
    ]