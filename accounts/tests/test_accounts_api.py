from decimal import Decimal

from model_mommy import mommy
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import Currency, Account


class ListAccountsTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        currency_a = mommy.make(Currency, code='AAA')
        mommy.make(Account, name='account_a', currency=currency_a, value=Decimal('1'))
        currency_b = mommy.make(Currency, code='BBB')
        mommy.make(Account, name='account_b', currency=currency_b, value=Decimal('2'))

    def test_list_accounts(self):
        url = reverse('accounts_v1:accounts-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)
        self.assertSetEqual({account['id'] for account in response.data['results']}, {'account_a', 'account_b'})

    def test_not_implemented(self):
        url = reverse('accounts_v2:accounts-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED, response.data)

