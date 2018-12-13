from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import Account
from payments.managers import PaymentManager
from utils.models import AmountField


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
