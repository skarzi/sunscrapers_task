"""Local settings
"""
from .base import *

SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='change$#zlco+@d$7fyp2wb#bcte&71k6h4_uqz4-(7xxni*#3^x6h9yme-pls',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}


# django rest framework
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

# django debug toolbar
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
# to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS += [ip[:-1] + '1']
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django extensions
IPYTHON_ARGUMENTS = [
    '--TerminalInteractiveShell.editing_mode=vi',
    '--TerminalInteractiveShell.editor=vim',
]

TEST_RUNNER = 'config.runner.PytestTestRunner'
