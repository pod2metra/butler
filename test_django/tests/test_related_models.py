from django import test
from django.core import urlresolvers
from test_django.link_sorter.models import Link, LinkStatistics
from test_django.tests.test_workflow import RestResourceTest


class DjangoOrmRestResourceTest(RestResourceTest):

    def __init__(self, methodName='runTest'):
        super(DjangoOrmRestResourceTest, self).__init__(methodName)
        self.url = urlresolvers.reverse(viewname='internal_v0.1_link_stat')

    def test_get_one(self):
        link, created = Link.objects.get_or_create(
            long_link='http://www.ostrovok.ru',
        )
        LinkStatistics.objects.get_or_create(
            link=link,
        )
        res = self.get(self.url)

        obj = res.deserialized_content[0]

        for field in ['link', 'created_count', 'redirect_count']:
            self.assertTrue(field in obj, field)






