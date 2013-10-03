import urllib
from django import test
import ujson


DATA_FORMATS = {
    'json': {
        'to_string': ujson.dumps,
        'from_string': ujson.loads
    }
}


def prepare_data(data, fmt):
    to_string = DATA_FORMATS[fmt]['to_string']
    data = to_string(data or {})
    return data


def prepare_url(filters, url):
    filters = filters or {}
    url = '{}?{}'.format(url, urllib.urlencode(filters))
    return url


def alter_response_with_deserialized_data(resp, fmt):
    to_python = DATA_FORMATS[fmt]['from_string']
    content = resp.content
    if content:
        resp.deserialized_content = to_python(resp.content)


class RestResourceTest(test.TestCase):

    def __init__(self, methodName='runTest'):
        super(RestResourceTest, self).__init__(methodName)
        self.client = test.Client()

    def put(self, url, filters=None, data=None, fmt='json'):
        content_type = 'application/{}'.format(fmt)
        data = prepare_data(data, fmt)
        url = prepare_url(filters, url)
        resp = self.client.put(url, data, content_type=content_type)
        alter_response_with_deserialized_data(resp, fmt)
        return resp

    def post(self, url, filters=None, data=None, fmt='json'):
        content_type = 'application/{}'.format(fmt)
        data = prepare_data(data, fmt)
        url = prepare_url(filters, url)
        resp = self.client.post(url, data, content_type=content_type)
        alter_response_with_deserialized_data(resp, fmt)
        return resp

    def delete(self, url, filters=None, fmt='json'):
        content_type = 'application/{}'.format(fmt)
        url = prepare_url(filters, url)
        resp = self.client.delete(url, content_type=content_type)
        alter_response_with_deserialized_data(resp, fmt)
        return resp

    def get(self, url, filters=None, fmt='json'):
        content_type = 'application/{}'.format(fmt)
        filters = filters or {}
        resp = self.client.get(url, filters, content_type=content_type)
        alter_response_with_deserialized_data(resp, fmt)
        return resp
