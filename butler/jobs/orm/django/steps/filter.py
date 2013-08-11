from butler.jobs.workflow import Step


class Filter(Step):

    def __init__(self, model_klass):
        super(Filter, self).__init__()
        self.model_klass = model_klass

    def run(self, request, **context):
        filters = request.GET or {}

        models = self.model_klass.objects.filter(**filters)

        return {
            'data': models
        }