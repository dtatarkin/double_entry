from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountViewSet(ListModelMixin, GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
