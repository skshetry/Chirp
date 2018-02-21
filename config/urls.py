"""Chirp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import RedirectView
from django.conf import settings
from django.templatetags.static import static as static_tag
import testapp
import accounts
import settings as user_settings
import user_profile
import feed.views as feed_views

urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^$', RedirectView.as_view(url='/home', permanent=False)),
    url(r'^settings/', include('settings.urls', namespace='settings')),
    url(r'^user/', include('user_profile.urls', namespace='user_profile')),
    url(r'^', include('search.urls', namespace='search')),
    url(r'favicon.ico/$', RedirectView.as_view(
        url=static_tag('img/favicon.png'),
        permanent=True)),
    url(r'posts/', include('posts.urls', namespace='posts')),
    url(r'home/', include('feed.urls', namespace='feeds')),
]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    from django.conf.urls.static import  static
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.errors.views.not_found'
handler500 = 'apps.errors.views.server_error'
handler403 = 'apps.errors.views.permission_denied'
handler400 = 'apps.errors.views.bad_request'
