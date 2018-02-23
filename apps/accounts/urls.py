from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from .views import UserLoginView, logout_view, signup, activate as activate_view

app_name = 'accounts'
urlpatterns = [
    url(r'signup/$', signup, name='signup'),
    url(r'^login/$', UserLoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate_view, name='activate'),
        
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt',
            success_url = reverse_lazy('accounts:password_reset_done'),
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html',
            success_url = reverse_lazy('accounts:password_reset_complete'),
        ),
        name='password_reset_confirm'),
    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
]
