from rest_framework import serializers

from . import models


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rate
        fields = (
            'date',
            'value',
            'type',
            'base_currency_code',
            'target_currency_code',
            'data',
        )
