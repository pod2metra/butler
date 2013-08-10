from collections import defaultdict
from django.conf import urls as urlconf
from butler.meta import InheritedMetaClass


class Api(object):
    __metaclass__ = InheritedMetaClass

    REVERSE_NAME_PATTERN = '{name}_{version}_{resource_name}'
    PATH_PATTERN = '{name}/{version}/{resource_name}/'

    def __init__(self, name, version, resources=None, inherits=None):
        super(Api, self).__init__()
        # TODO: if None take from app name
        self.name = name
        self.version = version
        self.resources = resources or []
        self.registry = defaultdict(list)
        self.inherits = inherits

    def register(self, *resources):
        self.resources = self.resources.extend(resources)

    @property
    def urls(self):
        return self.get_urls()

    def get_urls(self):
        self.__apply_inheritance(self.inherits)
        urls = urlconf.patterns('',)

        for resource in self.resources:
            urls += self.get_resource_urls(resource)

        return urls

    def get_default_resource_urls(self, resource):

        resource_name = resource.name
        pattern_parameters = {
            'name': self.name,
            'version': self.version,
            'resource_name': resource_name,
        }
        reverse_name = self.REVERSE_NAME_PATTERN.format(**pattern_parameters)
        path = self.PATH_PATTERN.format(**pattern_parameters)
        return [urlconf.url(path, resource.dispatch, name=reverse_name)]

    def get_resource_urls(self, resource):
        urls = resource.get_urls(self.name, self.version)

        if urls:
            return urls

        return self.get_default_resource_urls(resource)

    def __apply_inheritance(self, api):
        if not api:
            return

        api_resource_index = {i.name: i for i in api.resources}
        for resource in self.resources:
            api_resource_index[resource.name] = resource
        self.resources = api_resource_index.values()
