from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('accounts.urls', namespace='accounts_v1')),
    path('v2/', include('accounts.urls', namespace='accounts_v2')),
    path('v1/', include('payments.urls', namespace='payments_v1')),
    url(r'v[0-9]+/', include('payments.urls', namespace='payments_v_')),
    # path('v1/', include('postings.urls', namespace='postings_v1')),
    # url(r'v[0-9]+/', include('postings.urls', namespace='postings_v_')),
]
