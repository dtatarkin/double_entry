from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from payments.models import Payment
from payments.serializers import PaymentSerializer
from postings.models import Posting
from postings.serializers import PostingSerializer
from utils.views import NotImplementedAPI


class PaymentViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    list_queryset = Posting.objects.order_by('-pk')

    def list(self, request, *args, **kwargs):
        # If this View can be used for different API version, we must check current API version.
        # This is an example how we can use one View for different API versions.
        if request.version == 'payments_v1':
            queryset = self.filter_queryset(self.list_queryset)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = PostingSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = PostingSerializer(queryset, many=True)
            return Response(serializer.data)
        raise NotImplementedAPI()

    def create(self, request, *args, **kwargs):
        # If this View can be used for different API version, we must check current API version.
        # This is an example how we can use one View for different API versions.
        if request.version == 'payments_v1':
            return super().create(request, *args, **kwargs)
        raise NotImplementedAPI()
