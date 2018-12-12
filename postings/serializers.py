from enum import Enum

from rest_framework import serializers

from postings.models import Posting


class PaymentDirection(Enum):
    OUTGOING = 'outgoing'
    INCOMING = 'incoming'


class PostingRelatedAccountField(serializers.SlugRelatedField):
    def __init__(self, slug_field='name', **kwargs):
        kwargs.setdefault('read_only', True)
        super().__init__(slug_field=slug_field, **kwargs)

    def get_attribute(self, instance):
        if self.source == 'payment.from_account' and instance.value < 0 \
                or self.source == 'payment.to_account' and instance.value > 0:
            raise serializers.SkipField()
        return super().get_attribute(instance)


class PostingSerializer(serializers.ModelSerializer):
    account = serializers.SlugRelatedField(slug_field='name', read_only=True)
    direction = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    from_account = PostingRelatedAccountField(source='payment.from_account')
    to_account = PostingRelatedAccountField(source='payment.to_account')

    class Meta:
        model = Posting
        fields = ['id', 'account', 'amount', 'direction', 'from_account', 'to_account']

    @staticmethod
    def get_direction(instance):
        if instance.value > 0:
            return PaymentDirection.INCOMING.value
        return PaymentDirection.OUTGOING.value

    @staticmethod
    def get_amount(instance):
        return str(abs(instance.value))
