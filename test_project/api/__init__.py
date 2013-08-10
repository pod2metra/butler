from django.conf import urls
import v0_1
import v0_2


urls = urls.patterns('',
    urls.url('', urls.include(v0_1.api.get_urls())),
    urls.url('', urls.include(v0_2.api.get_urls())),
)