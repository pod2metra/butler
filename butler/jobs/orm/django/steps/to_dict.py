from django.forms import model_to_dict
from butler.jobs.workflow import Step


class ToDict(Step):
    def __init__(self, allowed_fields=None):
        super(ToDict, self).__init__()
        self.allowed_fields = allowed_fields

    def model_to_dict(self, model, fields):
        model_dict = model_to_dict(model)
        if fields is None:
            return model_dict
        keys = set(model_dict.keys())
        to_delete = keys - self.allowed_fields
        for key in to_delete:
            model_dict.pop(key)
        return model_dict

    def run(self, data, resource, **context):
        allowed_fields = self.allowed_fields
        if not allowed_fields:
            allowed_fields = getattr(resource._meta, 'allowed_fields', None)

        return {
            'data': [
                self.model_to_dict(model, allowed_fields) for model in data
            ]
        }