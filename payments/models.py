from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models, transaction

from accounts.models import Account
from postings.models import Posting
from utils.models import AmountField


class PaymentManager(models.Manager):
    """Custom Manager with ability to proper payment creation."""

    @transaction.atomic
    def create_payment(self, from_account_pk: int, to_account_pk: int, value: Decimal):
        with transaction.atomic():
            if from_account_pk == to_account_pk:
                raise ValidationError('Unable to create payment for the same account', code='same_account')

            # Order Accounts so that first returns `from_account`
            order_by = 'pk' if from_account_pk < to_account_pk else '-pk'
            # Lock both Accounts in same time to avoid race conditions. Also lock related Currency (just in case).
            accounts = Account.objects.filter(
                pk__in=[from_account_pk, to_account_pk]
            ).select_related('currency').select_for_update(of='currency').order_by(order_by)
            accounts = list(accounts)
            # Both Accounts must exists
            if len(accounts) != 2:
                raise Account.DoesNotExist
            from_account, to_account = accounts

            if value <= 0:
                raise ValidationError('Payment value must be greater than zero', code='invalid_value')

            if from_account.currency != to_account.currency:
                raise ValidationError('Account currency must be the same.', code='invalid_currency')

            if from_account.value < value:
                raise ValidationError('Insufficient funds for an account {}'.format(from_account), code='no_funds')

            if to_account.value + value > settings.AMOUNT_VALUE_MAX:
                raise ValidationError('Value overflow for an account {}'.format(to_account), code='overflow')

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


class Payment(models.Model):
    """
    Represents Money transfer between two Accounts

    Representation of business transaction that will produce double entries — it represents a complete unit of work.
    I.e. all :class:`postings.models.Posting` entries associated with the :class:`Payment` entry must be successfully
    completed or none must be completed.
    The numerical sum of all `Posting` entries associated with a `Payment` entry must also equal zero.

    Notes

     - In a real project, this model is better renamed and treated as a transaction.
     - This model denormalize database schema for simplicity and performance.

    Attributes

     - from_account (:class:`accounts.models.Account`): Source Account.
     - to_account (:class:`accounts.models.Account`): Destination Account.
     - value (`Decimal`): Transferred amount. Must be greater than zero.

    """

    from_account = models.ForeignKey(Account, related_name='payments_from', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='payments_to', on_delete=models.CASCADE)
    value = AmountField(validators=[MinValueValidator(Decimal(1)/(10**settings.AMOUNT_DECIMAL_PLACES))])

    objects = PaymentManager()
