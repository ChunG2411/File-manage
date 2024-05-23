import re
import os
from django.conf import settings


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
    path = path.split('media/')[-1].replace('/', '\\')
    return os.path.join(settings.MEDIA_ROOT, path)
