import re
import os
from django.conf import settings
from functools import wraps
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.shortcuts import redirect


def check_validate(string):
    pattern = r'[!@#$%^&*(),.?":{}|<>]'
    if re.search(pattern, string):
        return True
    return False


def get_path_url(obj, path=[]):
    path = [[obj.name, obj.id]]
    if obj.parent:
        return get_path_url(obj.parent, path) + path
    else:
        return path


def get_path_file(path):
    path = path.split('media/')[-1]
    return os.path.join(settings.MEDIA_ROOT, path)


def token_blacklist_check(dispatch_func):
    def wrapper(self, request, *args, **kwargs):
        # token = self.request.META.get('HTTP_REFRESH', '')
        # try:
        #     outstanding_token = OutstandingToken.objects.get(token=token)
        #     BlacklistedToken.objects.get(token=outstanding_token)
        #     return redirect('blacklist_res')
        
        # except Exception as e:
        #     return dispatch_func(self, request, *args, **kwargs)
        return dispatch_func(self, request, *args, **kwargs)
    return wrapper


def check_token_blacklisted(view_class):
    view_class.dispatch = wraps(view_class.dispatch)(token_blacklist_check(view_class.dispatch))
    return view_class