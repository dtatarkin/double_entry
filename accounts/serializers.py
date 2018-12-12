from rest_framework import serializers

from accounts.models import Account
from utils.serializers import AmountField


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='name')
    balance = AmountField(source='value', read_only=True)
    currency = serializers.SlugRelatedField(slug_field='code', read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'owner', 'balance', 'currency']
