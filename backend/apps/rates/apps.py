from django.apps import AppConfig


class RatesConfig(AppConfig):
    name = 'apps.rates'
    verbose_name = 'Rates'

    def ready(self):
        pass
