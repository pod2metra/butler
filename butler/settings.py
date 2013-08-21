try:
    from django.conf import settings
except ImportError:
    settings = {}
else:
    if not settings.configured:
        settings.configure()


def ga(name, default):
    try:
        return getattr(settings, name, default)
    except ImportError:
        return default

DEBUG = ga('BUTLER_DEBUG', None)

if DEBUG is None:
    DEBUG = ga('DEBUG', False)

DATE_TIME_FORMAT = ga('BUTLER_DATE_TIME_FORMAT', '%Y-%m-%d %H:%M:%S')
DATE_FORMAT = ga('BUTLER_DATE_FORMAT', '%Y-%m-%d')

FILTER_SEPARATOR = '__'
