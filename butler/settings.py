try:
    from django.conf import settings
except ImportError:
    settings = {}


def ga(name, default):
    return getattr(settings, name, default)

DEBUG = ga('BUTLER_DEBUG', None)

if DEBUG is None:
    DEBUG = ga('DEBUG', False)

DATE_TIME_FORMAT = ga('BUTLER_DATE_TIME_FORMAT', '%Y-%m-%d %H:%M:%S')
DATE_FORMAT = ga('BUTLER_DATE_FORMAT', '%Y-%m-%d')