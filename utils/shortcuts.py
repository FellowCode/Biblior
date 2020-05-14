import urllib

from django.shortcuts import redirect
from django.urls import reverse


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def build_url(*args, **kwargs):
    get = kwargs.pop('get', {})
    url = reverse(*args, kwargs=kwargs)
    if get:
        url += '?' + urllib.parse.urlencode(get)
    return url

def iredirect(viewname, **kwargs):
    return redirect(build_url(viewname, **kwargs))