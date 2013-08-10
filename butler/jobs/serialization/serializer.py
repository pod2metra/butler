from butler.jobs.exceptions import ButlerException
from butler.jobs.workflow import Step


class UnidentifiedFormat(ButlerException):
    def as_response(self, request, context):
        return super(UnidentifiedFormat, self).as_response(request, context)


class ContentTypeSerializer(Step):

    def __init__(self, force_format=None, default_format=None):
        super(ContentTypeSerializer, self).__init__()
        self.format = force_format
        self.default_format = default_format

    def run(self, request, **kwargs):

        if not self.format:
            self.format = request.REQUEST.get('format', None)

        if not self.format:
            content_type = request.META.get('CONTENT_TYPE', None)
            self.format = content_type.split('/')[-1]

        if not self.format:
            self.format = self.default_format

        if not self.format:
            raise UnidentifiedFormat(request, kwargs)

        return kwargs