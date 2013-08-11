from django.forms import model_to_dict
from butler.jobs.workflow import Step


class ToDict(Step):
    def run(self, data, **context):
        return {
            'data': [model_to_dict(model) for model in data]
        }