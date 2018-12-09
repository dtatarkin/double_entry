from decimal import Decimal

from django.conf import settings
from django.db import models
from model_mommy import mommy
from model_mommy.generators import default_mapping


class DefaultCharField(models.CharField):
    """
    https://docs.djangoproject.com/en/2.1/ref/databases/#character-fields
    """

    MAX_LENGTH = 254

    def __init__(self,  *args, **kwargs):
        kwargs.setdefault('max_length', self.MAX_LENGTH)
        super().__init__(*args, **kwargs)


class AmountField(models.DecimalField):
    def __init__(self,  *args, **kwargs):
        kwargs.setdefault('max_digits', settings.AMOUNT_MAX_DIGITS)
        kwargs.setdefault('decimal_places', settings.AMOUNT_DECIMAL_PLACES)
        kwargs.setdefault('default', Decimal(0))
        super().__init__(*args, **kwargs)


mommy.generators.add(DefaultCharField, default_mapping[models.CharField])
mommy.generators.add(AmountField, default_mapping[models.DecimalField])
