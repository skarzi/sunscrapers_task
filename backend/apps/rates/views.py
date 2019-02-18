import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import (
    mixins,
    viewsets,
)

from . import (
    models,
    serializers,
)


class RateViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet,
):
    serializer_class = serializers.RateSerializer

    def get_queryset(self):
        return models.Rate.objects.raw('''
            SELECT DISTINCT ON (rates_rate.target_currency_code)
                rates_rate.id,
                rates_rate.base_currency_code,
                rates_rate.target_currency_code,
                rates_rate.value,
                rates_rate.date,
                rates_rate.type,
                rates_rate.date
            FROM rates_rate INNER JOIN (
                SELECT
                    rates_rate.target_currency_code,
                    MAX(rates_rate.date) as date
                FROM rates_rate
                GROUP BY rates_rate.target_currency_code
            ) as latest
            ON rates_rate.date = latest.date;
        ''')

    @method_decorator(cache_page(datetime.timedelta(hours=3).seconds))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)
