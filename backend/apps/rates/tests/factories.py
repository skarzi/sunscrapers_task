import datetime

import factory

from factory import fuzzy


def generate_data_for(instance):
    return {
        'link': 'http://www.knights.that/say/ni?ni=ni',
        'title': f'{instance} {instance.date} ECB Reference rate',
        'country': 'U2',
        'description': "Testing description.",
        'language_code': 'en',
        'institution_code': 'ECB'
    }


class RateFactory(factory.django.DjangoModelFactory):
    date = fuzzy.FuzzyDateTime(
        datetime.datetime(2019, 2, 2, tzinfo=datetime.timezone.utc),
    )
    value = fuzzy.FuzzyDecimal(10**(-15), 10**3, precision=16)
    target_currency_code = fuzzy.FuzzyChoice(
        choices=['KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON'],
    )
    data = factory.LazyAttribute(generate_data_for)
    type = 'Reference Rate'
    base_currency_code = 'EUR'

    class Meta:
        model = 'rates.Rate'
