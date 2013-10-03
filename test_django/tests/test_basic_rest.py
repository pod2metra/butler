import ujson
from butler import settings
from django import test
from django.core import urlresolvers
from test_django.link_sorter.models import Link
from test_django.tests.test_workflow import RestResourceTest


class DjangoOrmRestResourceTest(RestResourceTest):

    LONG_LINK = u'http://sergey.co.il'

    NEW_OBJECT_DATA = {
        'long_link': LONG_LINK
    }

    def __init__(self, methodName='runTest'):
        super(DjangoOrmRestResourceTest, self).__init__(methodName)
        self.url = urlresolvers.reverse(viewname='internal_v0.1_link')

    def convert_response(self, data):
        data = ujson.loads(data)
        return data

    def test_get_none(self):
        self.assertEquals(self.url, '/internal/v0.1/link/')
        data = self.get(self.url)
        self.assertEquals(data.status_code, 200)
        self.assertEquals(data.content, '[]')

    def test_get_one(self):
        Link.objects.create(
            **self.NEW_OBJECT_DATA
        )
        data = self.get(self.url)
        self.assertEquals(data.status_code, 200)
        self.assertNotEquals(data.content, '[]')

        python_data = data.deserialized_content

        self.assertEquals(len(python_data), 1)

        obj = python_data[0]

        for field in ['long_link', 'id', 'created_at']:
            msg = '{} not found in {}'
            self.assertTrue(field in obj, msg.format(
                field, obj
            ))

    def test_put_shit(self):
        data = self.put(
            self.url,
            data=self.NEW_OBJECT_DATA
        )
        self.assertEquals(data.status_code, 200)
        self.assertEquals(data.content, '{"updated": 0}')

    def test_post_one(self):
        data = self.post(
            self.url,
            data=self.NEW_OBJECT_DATA
        )
        link = Link.objects.all()[0]
        self.assertEquals(data.status_code, 200)
        expected_data = [
            {
                u'created_at': u'{}'.format(link.created_at.strftime(
                    settings.DATE_TIME_FORMAT)),
                u'long_link': self.LONG_LINK,
                u'id': 1,
                u'stat': [],
            }
        ]
        response_data = self.convert_response(data.content)
        self.assertListEqual(expected_data, response_data)

    def test_delete_one(self):
        data = self.post(
            self.url,
            data=self.NEW_OBJECT_DATA
        )
        link = Link.objects.all()[0]
        self.assertEquals(data.status_code, 200)
        expected_data = [
            {
                u'created_at': u'{}'.format(link.created_at.strftime(
                    settings.DATE_TIME_FORMAT)),
                u'long_link': self.LONG_LINK,
                u'id': 1,
                u'stat': [],
            }
        ]
        response_data = self.convert_response(data.content)
        self.assertListEqual(expected_data, response_data)
        data = self.delete(
            self.url,
            filters={
                'id': 1
            }
        )
        self.assertEquals(data.status_code, 200)
        self.assertEquals(
            data.content,
            '{"deleted": 1}'
        )
