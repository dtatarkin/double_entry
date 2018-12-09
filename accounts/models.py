from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _

from accounts.consts import ERROR_INVALID_CURRENCY_CODE
from utils.models import DefaultCharField, AmountField


class CurrencyCodeValidator(RegexValidator):
    regex = r'^[A-Z]{3}$'
    message = _(ERROR_INVALID_CURRENCY_CODE)


class Currency(models.Model):
    code = DefaultCharField(max_length=3, validators=[CurrencyCodeValidator()])


class Account(models.Model):
    name = DefaultCharField(unique=True)
    owner = models.ForeignKey(get_user_model(), null=True, blank=True, related_name='accounts',
                              on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, related_name='accounts', on_delete=models.CASCADE)
    value = AmountField()  # Denormalize database for simplicity and performance
