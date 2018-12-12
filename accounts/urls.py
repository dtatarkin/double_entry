from django.urls import path, include
from rest_framework import routers

from accounts.apps import AccountsConfig
from accounts.views import AccountViewSet

app_name = AccountsConfig.name

router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='accounts')

urlpatterns = [
    path('', include(router.urls)),
]
