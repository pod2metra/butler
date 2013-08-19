from butler.jobs.workflow import Step


class Create(Step):

    def __init__(self, model_klass):
        super(Create, self).__init__()
        self.model_klass = model_klass
        self.fields = {}

        for field in self.model_klass._meta.fields:
            self.fields[field.name] = field

    def run(self, request, data, **context):
        create_fields = {}

        for field, value in data.items():
            if field in self.fields:
                create_fields[field] = self.fields[field].to_python(value)

        obj = self.model_klass.objects.create(
            **create_fields
        )
        return {
            "created": [obj]
        }

