from django.conf import settings
from rest_framework import serializers


class AmountField(serializers.DecimalField):
    def __init__(self,  *args, **kwargs):
        kwargs.setdefault('max_digits', settings.AMOUNT_MAX_DIGITS)
        kwargs.setdefault('decimal_places', settings.AMOUNT_DECIMAL_PLACES)
        super().__init__(*args, **kwargs)
