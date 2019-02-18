from django.contrib.postgres import fields as postgres_fields
from django.db import models


class Rate(models.Model):
    date = models.DateTimeField()
    value = models.DecimalField(max_digits=32, decimal_places=16)
    type = models.CharField(max_length=64)
    base_currency_code = models.CharField(max_length=3)
    target_currency_code = models.CharField(max_length=3)
    data = postgres_fields.JSONField()

    class Meta:
        unique_together = ('date', 'target_currency_code')

    def __str__(self):
        return (
            f'1 {self.target_currency_code} = {self.value} '
            f'{self.base_currency_code}'
        )
