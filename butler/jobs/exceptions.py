from django.conf import settings
from django.http import HttpResponse


# TODO: add debug info in DEBUG mode
class ButlerException(Exception):
    def __init__(self, *args, **kwargs):
        super(ButlerException, self).__init__(*args, **kwargs)

    def as_response(self, request, resource, context):
        raise NotImplementedError()


class ExceptionWrapper(ButlerException):
    def __init__(self, exception):
        super(ExceptionWrapper, self).__init__()
        self.exception = exception

    def as_response(self, request, resource, context):
        import traceback
        tb = traceback.format_exc()

        if not settings.DEBUG:
            return HttpResponse(
                content='Debug mode exception \n\n{0}'.format(
                    tb
                )
            )

        return HttpResponse(
            content='Exception \n\n{0}'.format(
                tb
            )
        )

