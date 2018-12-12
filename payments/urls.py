from django.urls import path, include
from rest_framework import routers

from payments.apps import PaymentsConfig
from payments.views import PaymentViewSet

app_name = PaymentsConfig.name

router = routers.DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls)),
]
