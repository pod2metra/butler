import datetime
import decimal
import json


class JsonSerializer(object):
    def to_string(self, data):

        def default_callback(val):
            if isinstance(val, datetime.date):
                return val.strftime('%Y-%m-%d')

            if isinstance(val, decimal.Decimal):
                return '{0:.2f}'.format(val)

            raise TypeError('Unable to serialize {} {}'.format(val, type(val)))

        return json.dumps(data, ensure_ascii=True, default=default_callback)

    def from_string(self, str_data):
        return json.loads(str_data)
