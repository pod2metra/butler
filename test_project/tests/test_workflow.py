import urllib
import ujson
from django import test
from butler.jobs.workflow import Workflow, Step


class TestStep1(Step):
    def __call__(self, **context):
        return super(TestStep1, self).__call__(**context)


class ResourceTest(test.TestCase):

    # FORMAT_SERIALIZER
    JSON_SERIALIZER = ujson.dumps

    # FORMAT_DESERIALIZER
    JSON_DESERIALIZER = ujson.loads

    def _get_data_worker(self, format, flag):
        s = 'deserializer' if flag else 'serializer'
        tag = '{}_{}'.format(format, s)
        try:
            return getattr(self, tag.upper())
        except AttributeError:
            raise Exception('Invalid {} format : {}'.format(s, format))

    def _get_serializer(self, format):
        return self._get_data_worker(format, False)

    def _get_deserializer(self, format):
        return self._get_data_worker(format, True)

    def _processing(self, url, method, get_params, body, format, status_code):
        client = test.Client()
        method_dict = {
            'get': client.get,
            'post': client.post,
            'put': client.put,
            'delete': client.delete,
        }
        try:
            method_foo = method_dict[method]
        except KeyError:
            raise Exception('Unkonwn method {}'.format(method))
        serialize_foo = self._get_serializer(format)
        deserialize_foo = self._get_deserializer(format)
        if get_params is not None and not isinstance(get_params, basestring):
            get_params = urllib.urlencode(get_params)
        if not (body is None or isinstance(body, basestring)):
            body = serialize_foo(body)
        if get_params:
            url = '{}?{}'.format(url, get_params)
        resp = method_foo(url)
        self.assertEqual(resp.status_code, status_code)
        content = resp.content
        if content:
            return deserialize_foo(resp.content)
        return content

    def put(self, url, get_params={}, data={}, format='json', status_code=200):
        return self._processing(
            url, 'put', get_params, data, format, status_code)

    def post(self, url, get_params={}, data={},
             format='json', status_code=200):
        return self._processing(
            url, 'post', get_params, data, format, status_code)

    def delete(self, url, get_params={}, data={},
               format='json', status_code=200):
        return self._processing(
            url, 'delete', get_params, data, format, status_code)

    def get(self, url, get_params={}, status_code=200):
        return self._processing(
            url, 'get', get_params, {}, 'json', status_code)


class WorkflowTest(ResourceTest):

    def test_shit(self):
        self.assertFalse(True)

    def test_link_getter(self):
        data = self.get('/internal/v0.1/link/')
