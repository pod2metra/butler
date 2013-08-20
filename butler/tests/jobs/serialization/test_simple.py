# coding=utf-8
from django.http import HttpRequest
from butler.jobs.serialization.exceptions import ParameterNotSpecified
from butler.jobs.serialization.simple import ToString
from butler.tests.helpers import raises
from nose2.tests._common import TestCase


class TestSerrialization(TestCase):

    def test_format_determinition_test_get_parameter(self):
        """ If request has GET parameter specified
            format is determined correctly """
        step = ToString()

        request = HttpRequest()

        formats = ['json', 'xml', 'yaml']

        for expected in formats:
            request.GET['format'] = expected
            actual = step.get_format(request)
            self.assertEqual(
                expected,
                actual,
                'Wrong format determined. Expected {} got {} instead.'.format(
                    expected, actual))

    def test_format_determinition_test_by_content_type(self):
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
            self.assertEqual(
                expected,
                actual,
                'Wrong format determined. Expected {} got {} instead.'.format(
                    expected, actual))

    def test_format_determinition_forced_setting(self):
        """ Test that forced setting override GET
        """
        expected = 'json'
        step = ToString(force_format=expected)

        request = HttpRequest()

        formats = ['json', 'xml', 'yaml']

        for fmt in formats:
            request.GET['format'] = fmt
            actual = step.get_format(request)
            self.assertEqual(
                expected,
                actual,
                'Wrong format determined. Expected {} got {} instead.'.format(
                    expected, actual))

    def test_default_format_setting(self):
        """ Test that default setting works
        """
        expected = 'json'
        step = ToString(default_format=expected)
        request = HttpRequest()
        actual = step.get_format(request)
        self.assertEqual(
            expected,
            actual,
            'Wrong format determined. Expected {} got {} instead.'.format(
                expected, actual))

    @raises(ParameterNotSpecified)
    def test_format_determinition_test_exception(self):
        """ Throws error if nothing is specified
        """
        step = ToString()
        request = HttpRequest()
        step.get_format(request)

    def test_serialization_json(self):
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
        now_str = datetime.datetime.strftime(now,
                                             format=settings.DATE_TIME_FORMAT)
        today_str = datetime.datetime.strftime(today,
                                               format=settings.DATE_FORMAT)
        expected = [
            '"string": "string"',
            '"ustring": "\u044b\u0444\u0432\u0444\u044b\u0432"',
            '"int": 23',
            '"decimal": 123.45',
            '"date": "{}"'.format(today_str),
            '"now": "{}"'.format(now_str)
        ]

        self.assertIn('result', context)
        actual = context['result']
        for e in expected:
            self.assertIn(
                e,
                actual,
                '"{}" is not found in "{}"'.format(expected, actual)
            )

    # TODO: Test xml and yaml serialization
