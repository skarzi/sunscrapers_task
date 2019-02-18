from django.conf import settings
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('rates/', include('apps.rates.urls', namespace='rates')),
]


if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
            *urlpatterns,
        ]

