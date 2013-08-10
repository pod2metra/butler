
class ButlerException(Exception):
    def __init__(self, *args, **kwargs):
        super(ButlerException, self).__init__(*args, **kwargs)

    def as_response(self, request, context):
        raise NotImplementedError()


class ExceptionWrapper(ButlerException):
    def __init__(self, exception):
        super(ExceptionWrapper, self).__init__()
        self.exception = exception