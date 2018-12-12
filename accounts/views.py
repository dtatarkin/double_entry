from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from accounts.models import Account
from accounts.serializers import AccountSerializer
from utils.views import NotImplementedAPI


class AccountViewSet(ListModelMixin, GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def list(self, request, *args, **kwargs):
        if request.version == 'accounts_v1':
            return super().list(request, *args, **kwargs)
        raise NotImplementedAPI()
