from butler.jobs.workflow import Step


class Limit(Step):

    def __init__(self, limit=None):
        super(Limit, self).__init__()
        self.limit = limit

    def run(self, request, data, resource, **context):
        limit = self.limit or getattr(resource._meta, 'limit', None)
        if limit:
            data = data[:limit]
        return {
            'data': data
        }

    def check_configurations(self, filter_fields):
        for conf in self.filter_configurations:
            if conf.required in filter_fields:
                return

        raise Exception('')
