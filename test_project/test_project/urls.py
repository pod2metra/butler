from django.conf import urls
from django.contrib import admin

admin.autodiscover()

import api

urlpatterns = urls.patterns('',
    urls.url('', urls.include(api.urls)),
)
