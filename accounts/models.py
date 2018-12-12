from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _

from accounts.consts import ERROR_INVALID_CURRENCY_CODE
from utils.models import DefaultCharField, AmountField


class CurrencyCodeValidator(RegexValidator):
    """
    Validates `value` against :attr:`regex` attribute

    :Example:

    >>> from accounts.models import CurrencyCodeValidator
    >>> validator = CurrencyCodeValidator()
    >>> validator('ABC')
    """

    regex = r'^[A-Z]{3}$'
    message = _(ERROR_INVALID_CURRENCY_CODE)


class Currency(models.Model):
    """
    Represents a single Currency

    Each of the :class:`Account` stores values in a specified Currency.
    This model used for easy adding new Currency without Source Code changes.

    Attributes

     - code (CharField): Three-letter uppercase currency code.
       Inspired by `ISO 4217 <https://en.wikipedia.org/wiki/ISO_4217>`_

    """

    code = DefaultCharField(max_length=3, validators=[CurrencyCodeValidator()], unique=True)


class Account(models.Model):
    """
    Represents an Account

    This model denormalize database by storing current value for simplicity and performance.

    Attributes

     - name (CharField): Unique name of an Account, e.g. `bob123`.
     - owner (get_user_model()): User who owns an Account.
     - currency (:class:`Currency`): Account Currency.
     - value (`Decimal`): Account current value.

    """

    name = DefaultCharField(unique=True)
    owner = models.ForeignKey(get_user_model(), null=True, blank=True, related_name='accounts',
                              on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, related_name='accounts', on_delete=models.CASCADE)
    value = AmountField()

    def __str__(self):
        return self.name
