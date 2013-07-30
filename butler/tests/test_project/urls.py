from django.conf import urls
from butler.future.api import Api
from butler.future.tests.test_project.api import v1, v2

api_v1 = Api(
    name='341',
    version='1',
    resources=[
        v1.resources.link.LinkResource,
        v1.resources.link_stat.LinkStatistics,
    ]
)

api_v2 = Api(
    name='lfg',
    version='2',
    inherits=api_v1,
    resources=[
        v2.resources.link.LinkResource,
    ]
)

urlpatterns = urls.patterns('',
    urls.url('echannel/api/', api_v2.urls + api_v1.urls),
)