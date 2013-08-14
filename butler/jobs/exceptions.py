from django.http import HttpResponse
from butler import settings


class ButlerException(Exception):
    def __init__(self, *args, **kwargs):
        super(ButlerException, self).__init__(*args, **kwargs)

    def as_response(self, request, resource, context):
        raise NotImplementedError()


class ExceptionWrapper(ButlerException):
    def __init__(self, exception, status_code=500):
        super(ExceptionWrapper, self).__init__()
        self.exception = exception
        self.status_code = status_code

    def as_response(self, request, resource, context):
        if settings.DEBUG:
            raise self.exception

        return HttpResponse(
            content='Exception',
            status=self.status_code
        )

