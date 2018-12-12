from decimal import Decimal

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Sum
from model_mommy import mommy

from accounts.models import Account, Currency
from payments.models import Payment
from postings.models import Posting


@pytest.mark.django_db(transaction=True)  # Note: Testing transactions
def test_create_payment():

    currency = mommy.make(Currency)

    from_account = mommy.make(Account, currency=currency, value=Decimal('100'))
    to_account = mommy.make(Account, currency=currency, value=Decimal('0.01'))

    payment = Payment.objects.create_payment(
        from_account_pk=from_account.pk, to_account_pk=to_account.pk, value=Decimal('100')
    )

    # Test from_account value
    from_account.refresh_from_db()
    assert from_account.value == Decimal('0')

    # Test to_account value
    to_account.refresh_from_db()
    assert to_account.value == Decimal('100.01')

    # Test posting balance
    assert Posting.objects.filter(payment=payment).count() == 2
    assert Posting.objects.filter(payment=payment).aggregate(sum=Sum('value'))['sum'] == 0


@pytest.mark.django_db(transaction=True)
class TestValidation:
    params = dict(
        test_create_payment_fail=('from_code,to_code', (
            ['AAA', 'BBB'],
        ))
    )

    @pytest.fixture(autouse=True)
    def setup(self):
        mommy.make(Currency, code='AAA')
        mommy.make(Currency, code='BBB')

    @pytest.mark.parametrize('from_code,to_code,from_value,to_value,value,exc_code', (
            ('AAA', 'BBB', Decimal('100'), Decimal('0.01'), Decimal('100'), 'invalid_currency'),
            ('AAA', 'AAA', Decimal('99'), Decimal('0.01'), Decimal('100'), 'no_funds'),
            ('AAA', 'AAA', settings.AMOUNT_VALUE_MAX, Decimal('0.01'), settings.AMOUNT_VALUE_MAX, 'overflow'),
            ('AAA', 'AAA', Decimal('100'), Decimal('100'), -Decimal('100'), 'invalid_value'),
    ))
    def test_create_payment_fail(self, from_code, to_code, from_value, to_value, value, exc_code):
        from_currency = Currency.objects.get(code=from_code)
        to_currency = Currency.objects.get(code=to_code)

        from_account = mommy.make(Account, currency=from_currency, value=from_value)
        to_account = mommy.make(Account, currency=to_currency, value=to_value)

        with pytest.raises(ValidationError) as exc_info:
            Payment.objects.create_payment(
                from_account_pk=from_account.pk, to_account_pk=to_account.pk, value=value
            )

        assert exc_info.value.code == exc_code


@pytest.mark.django_db(transaction=True)
def test_create_payment_invalid_account():
    from_account = mommy.make(Account)
    with pytest.raises(Account.DoesNotExist):
        Payment.objects.create_payment(
            from_account_pk=from_account.pk, to_account_pk=from_account.pk+1, value=Decimal('0.01')
        )


@pytest.mark.django_db(transaction=True)
def test_create_payment_same_account():
    from_account = mommy.make(Account)
    with pytest.raises(ValidationError) as exc_info:
        Payment.objects.create_payment(
            from_account_pk=from_account.pk, to_account_pk=from_account.pk, value=Decimal('0.01')
        )
    assert exc_info.value.code == 'same_account'
