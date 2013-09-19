from butler.jobs.workflow import Step
from butler.jobs.orm.django import utils


class ToDict(Step):

    def __init__(self, model_klass=None, allowed_fields=None):
        super(ToDict, self).__init__()
        self.allowed_fields = allowed_fields
        if model_klass:
            utils.build_model_to_dict_description(model_klass)

    def run(self, data, resource, **context):
        resource_model_to_dict = getattr(resource, 'model_to_dict', None)
        is_callable = hasattr(resource_model_to_dict, '__call__')

        if resource_model_to_dict and is_callable:
            model_to_dict = resource_model_to_dict
        else:
            model_to_dict = utils.model_to_dict

        allowed_fields = self.allowed_fields
        if not allowed_fields:
            allowed_fields = getattr(resource._meta, 'allowed_fields', None)

        return {
            'data': [
                model_to_dict(model, allowed_fields) for model in data
            ]
        }