from butler.jobs.workflow import Step


class Update(Step):

    def __init__(self, model_klass):
        super(Update, self).__init__()
        self.model_klass = model_klass
        self.fields = {}

        for field in self.model_klass._meta.fields:
            self.fields[field.name] = field

    def run(self, request, filtered, data, **context):
        update_fields = {}

        for field, value in data.items():
            if field in self.fields:
                update_fields[field] = self.fields[field].to_python(value)

        count = data.update(
            **update_fields
        )
        return {
            "data": {
                "updated": count or 0
            }
        }
