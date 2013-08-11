from django.http import HttpResponse
from butler.jobs.exceptions import ButlerException


class ParameterNotSpecified(ButlerException):
    def as_response(self, request, resource, context):
        return HttpResponse(
            content=u"Content-type, get parameter and "
                    u"default behaviour indefined"
        )


class NoSerializerFound(ButlerException):
    def __init__(self, fmt):
        super(NoSerializerFound, self).__init__()
        self.fmt = fmt

    def as_response(self, request, resource, context):
        return HttpResponse(
            content=u"Unidentified format {}."
        )

