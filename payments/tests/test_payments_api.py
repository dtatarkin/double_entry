from decimal import Decimal

from django.conf import settings
from model_mommy import mommy
from parameterized import parameterized
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from accounts.models import Currency, Account
from postings.models import Posting
from postings.serializers import PaymentDirection
from utils.views import reverse_querystring


class CreatePaymentTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.currency_a = mommy.make(Currency, code='AAA')
        cls.currency_b = mommy.make(Currency, code='BBB')

    def test_create_payment(self):
        mommy.make(Account, currency=self.currency_a, name='bob123', value=Decimal('100'))
        mommy.make(Account, currency=self.currency_a, name='alice456', value=Decimal('0.01'))
        url = reverse('payments_v1:payments-list')
        data = dict(
            from_account='bob123',
            to_account='alice456',
            value=Decimal('100'),
        )
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        # Test list
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['count'], 2)
        results = response.data['results']
        self.assertEqual(len(results), 2)

        self.assertEqual(results[0]['amount'], results[1]['amount'])

        posting = results[0]
        self.assertEqual(Decimal(posting['amount']), data['value'])
        self.assertEqual(posting['direction'], PaymentDirection.INCOMING.value)
        self.assertEqual(posting['account'], 'alice456')
        self.assertEqual(posting['from_account'], 'bob123')
        self.assertNotIn('to_account', posting)

        posting = results[1]
        self.assertEqual(Decimal(posting['amount']), data['value'])
        self.assertEqual(posting['direction'], PaymentDirection.OUTGOING.value)
        self.assertEqual(posting['account'], 'bob123')
        self.assertEqual(posting['to_account'], 'alice456')
        self.assertNotIn('from_account', posting)

    def test_pagination(self):
        mommy.make(Posting, _quantity=2)
        url = reverse('payments_v1:payments-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 2)

        url = reverse_querystring('payments_v1:payments-list', query_kwargs=dict(offset=1))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(len(response.data['results']), 1)

    def test_invalid_account(self):
        mommy.make(Account, currency=self.currency_a, name='bob123', value=Decimal('100'))
        url = reverse('payments_v1:payments-list')
        data = dict(
            from_account='bob123',
            to_account='alice456',
            value=Decimal('100'),
        )
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertIn('to_account', response.data, response.data)
        errors = response.data['to_account']
        self.assertEqual(len(errors), 1)
        self.assertEqual(response.data['to_account'][0].code, 'does_not_exist', response.data)

    def test_same_account(self):
        mommy.make(Account, currency=self.currency_a, name='bob123', value=Decimal('100'))
        url = reverse('payments_v1:payments-list')
        data = dict(
            from_account='bob123',
            to_account='bob123',
            value=Decimal('100'),
        )
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertIn('non_field_errors', response.data, response.data)
        errors = response.data['non_field_errors']
        self.assertEqual(len(errors), 1)
        self.assertEqual(response.data['non_field_errors'][0].code, 'same_account', response.data)

    @parameterized.expand((
        ('AAA', 'BBB', Decimal('100'), Decimal('0.01'), Decimal('100'), 'invalid_currency', 'non_field_errors'),
        ('AAA', 'AAA', Decimal('99'), Decimal('0.01'), Decimal('100'), 'no_funds', 'non_field_errors'),
        ('AAA', 'AAA', settings.AMOUNT_VALUE_MAX, Decimal('0.01'), settings.AMOUNT_VALUE_MAX, 'overflow',
         'non_field_errors'),
        ('AAA', 'AAA', Decimal('100'), Decimal('100'), -Decimal('100'), 'min_value', 'value'),
    ))
    def test_create_payment_fail(self, from_code, to_code, from_value, to_value, value, exc_code, key):
        from_currency = Currency.objects.get(code=from_code)
        to_currency = Currency.objects.get(code=to_code)

        mommy.make(Account, currency=from_currency, name='bob123', value=from_value)
        mommy.make(Account, currency=to_currency, name='alice456', value=to_value)

        url = reverse('payments_v1:payments-list')
        data = dict(
            from_account='bob123',
            to_account='alice456',
            value=value,
        )
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertIn(key, response.data, response.data)
        errors = response.data[key]
        self.assertEqual(len(errors), 1)
        self.assertEqual(response.data[key][0].code, exc_code, response.data)

    def test_list_not_implemented(self):
        url = reverse('payments_v_:payments-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED, response.data)

    def test_create_not_implemented(self):
        url = reverse('payments_v_:payments-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED, response.data)
