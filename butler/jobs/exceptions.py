
class ButlerException(Exception):
    def __init__(self, *args, **kwargs):
        super(ButlerException, self).__init__(*args, **kwargs)


class ButlerResponseException(ButlerException):
    def __init__(self, fmt, *args, **kwargs):
        super(ButlerResponseException, self).__init__(*args, **kwargs)
        self.fmt = fmt


class ButlerErrorResponce(ButlerResponseException):
    pass
