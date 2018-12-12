from django.core import exceptions
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, ErrorDetail

from accounts.models import Account
from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    from_account = serializers.SlugRelatedField(slug_field='name', queryset=Account.objects.all())
    to_account = serializers.SlugRelatedField(slug_field='name', queryset=Account.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        try:
            instance = Payment.objects.create_payment(
                from_account_pk=validated_data['from_account'].pk,
                to_account_pk=validated_data['to_account'].pk,
                value=validated_data['value'],
            )
        except exceptions.ValidationError as exc:
            raise ValidationError(dict(non_field_errors=[ErrorDetail(exc.message, code=exc.code)]))
        return instance
