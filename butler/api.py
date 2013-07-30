from collections import defaultdict
from django.conf import urls as urlconf


class Api(object):
    REVERSE_NAME_PATTERN = '{name}_{version}_{resource_name}'
    PATH_PATTERN = '{name}/{version}/{resource_name}'

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
            urls.append(self.get_resource_urls(resource))

        return urls

    def get_default_resource_urls(self, resource):
        urls = urlconf.patterns('')
        resource_name = resource._meta.name
        pattern_parameters = {
            'name': self.name,
            'version': self.version,
            'resource_name': resource_name,
        }
        reverse_name = self.REVERSE_NAME_PATTERN.format(**pattern_parameters)
        path = self.PATH_PATTERN.format(**pattern_parameters)
        urls.append(
            urlconf.url(path, resource.dispatch, reverse_name)
        )
        return urls

    def get_resource_urls(self, resource):
        urls = resource.get_urls(self.name, self.version)

        if urls:
            return urls

        return self.get_default_resource_urls(resource)

    def __apply_inheritance(self, api):
        api_resource_index = {i._meta.name: i for i in api.resources}
        for resource in self.resources:
            api_resource_index[resource._meta.name] = resource
        self.resources = api_resource_index.values()
