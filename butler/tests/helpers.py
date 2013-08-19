from functools import wraps


def raises(exc_klass):
    def decorator(func):

        @wraps(func)
        def test_wraps(*args, **kwargs):
            no_exception = False
            try:
                func(*args, **kwargs)
                no_exception = True
            except Exception as e:
                if not isinstance(e, exc_klass):
                    assert False, 'Wrong exception was thrown, expected {} got {} instead'.format(
                        exc_klass, e
                    )
            if no_exception:
                assert False, 'No exception was thrown, expected {}'.format(
                    exc_klass
                )
        return test_wraps

    return decorator

