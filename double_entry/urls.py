from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

swagger_view = get_swagger_view(title='double_entry API')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('accounts.urls', namespace='accounts_v1')),
    path('v1/', include('payments.urls', namespace='payments_v1')),
    url(r'v[0-9]+/', include('payments.urls', namespace='payments_v_')),
    path('swagger/', swagger_view, name='swagger'),
]
