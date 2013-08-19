# coding=utf-8
from functools import wraps
from django.http import HttpRequest
from butler.jobs.serialization.exceptions import ParameterNotSpecified
from butler.jobs.serialization.simple import ToString


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


def test_format_determinition_test_get_parameter():
    """ If request has GET parameter specified format is determined correctly
    """
    step = ToString()

    request = HttpRequest()

    formats = ['json', 'xml', 'yaml']

    for expected in formats:
        request.GET['format'] = expected
        actual = step.get_format(request)
        assert expected == actual, 'Wrong format determined. Expected {} got {} instead.'.format(expected, actual)


def test_format_determinition_test_by_content_type():
    """ If request has GET parameter specified format is determined correctly
    """
    step = ToString()

    request = HttpRequest()

    formats = [
        'application/json',
        'application/xml',
        'application/yaml'
    ]

    for content_type in formats:
        request.META['CONTENT_TYPE'] = content_type
        expected = content_type.split('/')[1]
        actual = step.get_format(request)
        assert expected == actual, 'Wrong format determined. Expected {} got {} instead.'.format(content_type, actual)


def test_format_determinition_forced_setting():
    """ Test that forced setting override GET
    """
    expected = 'json'
    step = ToString(force_format=expected)

    request = HttpRequest()

    formats = ['json', 'xml', 'yaml']

    for fmt in formats:
        request.GET['format'] = fmt
        actual = step.get_format(request)
        assert expected == actual, 'Wrong format determined. Expected {} got {} instead.'.format(expected, actual)


def test_default_format_setting():
    """ Test that default setting works
    """
    expected = 'json'
    step = ToString(default_format=expected)
    request = HttpRequest()
    actual = step.get_format(request)
    assert expected == actual, 'Wrong format determined. Expected {} got {} instead.'.format(expected, actual)


@raises(ParameterNotSpecified)
def test_format_determinition_test_exception():
    """ Throws error if nothing is specified
    """
    step = ToString()
    request = HttpRequest()
    step.get_format(request)


def test_serialization_json():
    """ Test data serialization
    """
    from decimal import Decimal
    import datetime
    from butler import settings

    step = ToString(force_format='json')
    request = HttpRequest()
    request.method = 'GET'
    today = datetime.date.today()
    now = datetime.datetime.now()
    data = {
        'decimal': Decimal('123.45'),
        'date': today,
        'now': now,
        'string': 'string',
        'ustring': u'ыфвфыв',
        'int': 23,
    }
    context = {
        'resource': None,
        'request': request,
        'data': data
    }
    context.update(step(**context))
    expected = [
        '"string": "string"',
        '"ustring": "\u044b\u0444\u0432\u0444\u044b\u0432"',
        '"int": 23',
        '"decimal": 123.45',
        '"date": "{}"'.format(
            ('{:' + settings.DATE_FORMAT + '}').format(today)
        ),
        '"now": "{}"'.format(
            ('{:' + settings.DATE_TIME_FORMAT + '}').format(now)
        )
    ]
    actual = context['result']
    for e in expected:
        assert e in actual, '"{}" is not found in "{}"'.format(e, actual)


# TODO: Test xml and yaml serialization