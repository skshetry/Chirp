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
from django.conf import settings
import testapp
import accounts
import settings as user_settings
import user_profile

urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^', include('testapp.urls')),
    url(r'^settings/', include('settings.urls', namespace='settings')),
    url(r'^user/', include('user_profile.urls', namespace='user_profile')),
]

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        from django.conf.urls.static import  static
        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.errors.views.not_found'
handler500 = 'apps.errors.views.server_error'
handler403 = 'apps.errors.views.permission_denied'
handler400 = 'apps.errors.views.bad_request'
