from _pydecimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext as _

from accounts.models import Account
from postings.models import Posting


class PaymentManager(models.Manager):
    """Custom Manager with ability to proper payment creation."""

    @transaction.atomic
    def create_payment(self, from_account_pk: int, to_account_pk: int, value: Decimal):
        if from_account_pk == to_account_pk:
            raise ValidationError('Unable to create payment for the same account', code='same_account')

        # Order Accounts so that first returns `from_account`
        order_by = 'pk' if from_account_pk < to_account_pk else '-pk'
        # Lock both Accounts in same time to avoid race conditions.
        # Also lock related Currency (just in case, for safety) although that not right really needed
        # and can be skipped for performance.

        accounts = Account.objects.filter(
            pk__in=[from_account_pk, to_account_pk]
        ).select_related('currency').select_for_update(of=['currency']).order_by(order_by)
        accounts = list(accounts)
        # Both Accounts must exists
        if len(accounts) != 2:
            raise Account.DoesNotExist
        from_account, to_account = accounts

        if value <= 0:
            raise ValidationError(_('Payment value must be greater than zero'), code='invalid_value')

        if from_account.currency != to_account.currency:
            raise ValidationError(_('Account currency must be the same.'), code='invalid_currency')

        if from_account.value < value:
            raise ValidationError(_('Insufficient funds for an account {}').format(from_account), code='no_funds')

        if to_account.value + value > settings.AMOUNT_VALUE_MAX:
            raise ValidationError(_('Value overflow for an account {}').format(to_account), code='overflow')

        # Create Payment
        payment = self.create(from_account=from_account, to_account=to_account, value=value)
        # Create Postings
        Posting.objects.create(payment=payment, account=from_account, value=-value)
        Posting.objects.create(payment=payment, account=to_account, value=value)
        # Change Account values accordingly
        from_account.value -= value
        from_account.save(update_fields=['value'])
        to_account.value += value
        to_account.save(update_fields=['value'])

        return payment
