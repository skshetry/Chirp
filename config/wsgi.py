"""
WSGI config for Chirp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
from django.conf import settings

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


app_path = os.path.dirname(os.path.abspath(__file__)).replace('/config', '')
sys.path.append(os.path.join(app_path, 'apps'))

application = get_wsgi_application()

if 'raven.contrib.django.raven_compat' in settings.INSTALLED_APPS:
    from raven.contrib.django.raven_compat.middleware.wsgi import Sentry
    application = Sentry(application)
