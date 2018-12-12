from urllib.parse import urlencode

from django.urls import reverse
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.exceptions import APIException


class NotImplementedAPI(APIException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    default_detail = _('Not implemented API version.')
    default_code = 'not_implemented'


def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    """
    Custom reverse to handle query strings.

    Usage: reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search', 'Bob'})
    """
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url
