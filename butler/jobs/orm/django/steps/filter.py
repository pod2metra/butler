from dateutil.parser import parse
from butler.jobs.workflow import Step


class Filter(Step):

    def __init__(self, model_klass):
        super(Filter, self).__init__()
        self.model_klass = model_klass

    def run(self, request, **context):
        filters =  {}

        for param, value in request.GET.iteritems():
            filters[param] = parse(value)

        models = self.model_klass.objects.filter(**filters)
        return {
            'data': models
        }