from collections import namedtuple
from butler import settings
from butler.jobs.workflow import Step


FilterConfiguration = namedtuple('FilterConfiguration', [
    'required', 'optional'
])


class ModelFilter(Step):

    def __init__(self, model_klass, filter_configurations=None):
        super(ModelFilter, self).__init__()
        self.model_klass = model_klass
        self.fields = {}

        for field in self.model_klass._meta.fields:
            self.fields[field.name] = field

        self.filter_configurations = filter_configurations

    def run(self, request, **context):
        filters = {}

        filter_fields = set()
        for key, value in request.GET.iteritems():
            filter_path = key.split(settings.FILTER_SEPARATOR)
            field_name = filter_path[0]
            if field_name in self.fields:
                filter_fields.add(field_name)
                filters[key] = self.fields[field_name].to_python(value)

        if self.filter_configurations:
            self.check_configurations(filter_fields)

        models = self.model_klass.objects.filter(
            **filters
        )
        return {
            'filtered': models
        }

    def check_configurations(self, filter_fields):
        for conf in self.filter_configurations:
            if conf.required in filter_fields:
                return

        raise Exception('')
