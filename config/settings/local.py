from .common import *


# Operating System Environment variables have precedence over variables defined in the .env file,
# that is to say variables from the .env files will only be used if not defined
# as environment variables.
env_file = str(ROOT_DIR.path('.env'))
print('Loading : {}'.format(env_file))
env.read_env(env_file)
print('The .env file has been loaded. See local.py for more information')


DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = env('DJANGO_SECRET_KEY',
                 default='^I.%;h&Oc4xa;w8#zh~]Jf7tgb1-V!V/t04YsT>UgMb2-&W|11')
# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = 'localhost'
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')

DATABASES = {
    'default': {  # moving to postgres
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chirp',
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}


# middleware and installed apps
# ------------------------------------------------------------------------------
# add dev related middleware here.
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# add development apps here
INSTALLED_APPS += [
    'debug_toolbar',
]

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', 'localhost', '192.168.100.3', '0.0.0.0']
ALLOWED_HOSTS = INTERNAL_IPS

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
