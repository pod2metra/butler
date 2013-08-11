from butler.jobs.helpers import RequestMethodSwitch
from butler.jobs.serialization import exceptions
from butler.jobs.serialization import serializers


class BaseStep(RequestMethodSwitch):
    def __init__(self, force_format=None, default_format=None):
        super(BaseStep, self).__init__({
            'PUT': self.perform,
            'POST': self.perform,
        })
        self.fmt = force_format
        self.default_format = default_format

    def get_format(self, request):
        if self.fmt:
            return self.fmt

        self.fmt = request.REQUEST.get('fmt', None)
        if self.fmt:
            return self.fmt

        content_type = request.META.get('CONTENT_TYPE', None)
        content_type_fmt = content_type.split('/')[-1]
        if content_type_fmt in serializers.registered:
            return self.fmt

        self.fmt = self.default_format
        if self.fmt:
            return self.fmt

        raise exceptions.ParameterNotSpecified()

    def get_serializer(self, request):
        fmt = self.get_format(request)

        serializer = serializers.registered.get(fmt, None)

        if not serializer:
            exceptions.NoSerializerFound(fmt)

        return serializer

    def perform(self, **context):
        raise NotImplementedError()


class ToString(BaseStep):

    def __init__(self, force_format=None, default_format=None):
        super(ToString, self).__init__(force_format, default_format)
        self.switch.update({
            'get': self.perform,
            'delete': self.perform
        })

    def perform(self, resource, request, data, **kwargs):
        serializer = self.get_serializer(request)
        return {
            'result': serializer.to_string(data)
        }


class FromString(BaseStep):

    def perform(self, resource, request, data, **kwargs):
        serializer = self.get_serializer(request)
        return {
            'result': serializer.from_string(data)
        }
