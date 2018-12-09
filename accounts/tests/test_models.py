from decimal import Decimal

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from model_mommy import mommy

from accounts.models import Currency, CurrencyCodeValidator, Account


@pytest.mark.parametrize('value', (
    '',
    'AB',
    'ABCD',
    'abc',
))
def test_currency_code_validator_invalid(value):
    validator = CurrencyCodeValidator()
    with pytest.raises(ValidationError) as exc_info:
        validator(value)
    assert exc_info.value.code == 'invalid'


def test_currency_code_validator_valid():
    validator = CurrencyCodeValidator()
    validator('ABC')


@pytest.mark.django_db
def test_currency_model_invalid():
    currency = Currency(code='A')
    with pytest.raises(ValidationError) as exc_info:
        currency.full_clean()
    assert 'code' in exc_info.value.error_dict
    assert len(exc_info.value.error_dict['code']) == 1
    assert exc_info.value.error_dict['code'][0].code == 'invalid'


@pytest.mark.parametrize('value,code', (
    [
        Decimal('{}.{}'.format(
            Decimal('1' * (settings.AMOUNT_MAX_DIGITS - settings.AMOUNT_DECIMAL_PLACES - 1)),
            Decimal('1' * (settings.AMOUNT_DECIMAL_PLACES + 1)),
        )),
        'max_decimal_places',
    ],
    [
        Decimal('{}.{}'.format(
            Decimal('1' * (settings.AMOUNT_MAX_DIGITS - settings.AMOUNT_DECIMAL_PLACES + 1)),
            Decimal('1' * (settings.AMOUNT_DECIMAL_PLACES - 1)),
        )),
        'max_whole_digits',
    ],
    [
        Decimal('{}.{}'.format(
            Decimal('1' * (settings.AMOUNT_MAX_DIGITS - settings.AMOUNT_DECIMAL_PLACES + 1)),
            Decimal('1' * settings.AMOUNT_DECIMAL_PLACES),
        )),
        'max_digits',
    ]
))
@pytest.mark.django_db
def test_account_model_value_invalid(value, code):
    account = Account(value=value)
    with pytest.raises(ValidationError) as exc_info:
        account.full_clean()
    assert 'value' in exc_info.value.error_dict
    assert len(exc_info.value.error_dict['value']) == 1
    assert exc_info.value.error_dict['value'][0].code == code


@pytest.mark.parametrize('value', (
    0,
    '{}.{}'.format(
        Decimal('1' * (settings.AMOUNT_MAX_DIGITS - settings.AMOUNT_DECIMAL_PLACES)),
        Decimal('1' * settings.AMOUNT_DECIMAL_PLACES),
    ),
))
@pytest.mark.django_db
def test_account_model_value_valid(value):
    account = mommy.make(Account, value=value)
    account.full_clean()
    account.save()
    account.refresh_from_db()
    assert account.value == Decimal(value)
