from django.db import models

from accounts.models import Account
from utils.models import AmountField


class Posting(models.Model):
    """
    Represents the actual accounting double entries

    Attributes

     - payment (:class:`payment.models.Payment`): Related payment.
     - account (:class:`accounts.models.Account`): Corresponding Account.
     - value (`Decimal`): The  amount that Account value changes. Positive amount increases Account value,
       negative - decreases.

    """

    payment = models.ForeignKey('payments.Payment', related_name='postings', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name='postings', on_delete=models.CASCADE)
    value = AmountField()
