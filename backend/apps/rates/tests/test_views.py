import datetime
import operator

from django.urls import reverse

import pytest

from rest_framework import status

from apps.rates import models

from . import factories


@pytest.mark.django_db
class TestRateViewSet:
    url = reverse('rates:rates-list')
    sample_data = {
        'base_currency_code': 'EUR',
        'data': {
            'country': 'U2',
            'description': (
                '1 EUR buys 74.47 Polish zloty (PLN) - The reference '
                'exchange rates are published both by electronic market '
                "information providers and on the ECB's website shortly "
                'after the concertation procedure has been completed. '
                'Reference rates are published according to the same '
                'calendar as the TARGET system.'
            ),
            'institution_code': 'ECB',
            'language_code': 'en',
            'link': (
                'http://www.ecb.europa.eu/stats/exchange/eurofxref/html/'
                'eurofxref-graph-pln.en.html?date=2019-02-12&rate=74.47'
            ),
            'title': '74.47 PLN = 1 EUR 2019-02-12 ECB Reference rate'
        },
        'date': '2019-02-12T14:15:00+01:00',
        'target_currency_code': 'PLN',
        'type': 'Reference rate',
        'value': '74.47'
    }

    def test_create_creates_new_Rate_when_data_valid(self, api_client):
        response = api_client.post(self.url, data=self.sample_data)
        assert response.status_code == status.HTTP_201_CREATED
        created_rate_qs = models.Rate.objects.filter(
            target_currency_code=response.data['target_currency_code'],
            date=response.data['date'],
        )
        assert created_rate_qs.count() == 1

    def test_create_creates_returns_HTTP_400_when_unique_together_constraint_doesnt_fulfilled(
            self,
            api_client,
    ):
        rate = factories.RateFactory.create()
        data = dict(self.sample_data)
        data['date'] = rate.date.isoformat(timespec='microseconds')
        data['target_currency_code'] = rate.target_currency_code
        response = api_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

    def test_list_returns_latests_rates_for_every_currency(self, api_client):
        old_rates = [
            factories.RateFactory.create(target_currency_code=f'C{i}')
            for i in range(3)
        ]
        new_rates = [
            factories.RateFactory(
                target_currency_code=rate.target_currency_code,
                date=rate.date + datetime.timedelta(days=1),
            )
            for rate in old_rates
        ]
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        results_pks = self._rates_pks(response.data, self._item_getter)
        assert results_pks == self._rates_pks(new_rates)

    @staticmethod
    def _rates_pks(rates, getter=getattr):
        def force_datetime_to_str(value):
            if isinstance(value, datetime.datetime):
                value = value.isoformat()
            if value.endswith('+00:00'):
                value = value[:-6] + 'Z'
            return value

        return {
            (
                getter(rate, 'target_currency_code'),
                force_datetime_to_str(getter(rate, 'date')),
            )
            for rate in rates
        }

    @staticmethod
    def _item_getter(mapping, key):
        return mapping[key]
