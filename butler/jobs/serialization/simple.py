from butler.jobs.serialization import exceptions
from butler.jobs.workflow import Step
from butler.jobs.serialization import serializers


class BaseStep(Step):
    def __init__(self, force_format=None, default_format=None):
        super(BaseStep, self).__init__()
        self.fmt = force_format
        self.default_format = default_format

    def get_format(self, request):
        if self.fmt:
            return self.fmt

        self.fmt = request.REQUEST.get('fmt', None)
        if self.fmt:
            return self.fmt

        content_type = request.META.get('CONTENT_TYPE', None)
        self.fmt = content_type.split('/')[-1]
        if self.fmt:
            return self.fmt

        self.fmt = self.default_format
        if self.fmt:
            return self.fmt

        raise exceptions.ParameterNotSpecified()

    def serializer(self, request):
        fmt = self.get_format(request)
        serializer = getattr(serializers, fmt, None)

        if not serializer:
            exceptions.NoSerializerFound(fmt)

        return serializer


class ToString(BaseStep):
    def run(self, resource, request, data, **kwargs):
        fmt = self.get_format(request)
        serializer = getattr(serializers, fmt, None)
        return {
            'result': serializer.to_string(data)
        }


class FromString(BaseStep):
    def run(self, resource, request, data, **kwargs):
        fmt = self.get_format(request)
        serializer = getattr(serializers, fmt, None)
        return {
            'result': serializer.from_string(data)
        }
