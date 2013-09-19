from butler.jobs.workflow import Step
from butler.jobs.orm.django import model_descriptions


class ToDict(Step):
    def __init__(self, model_klass=None, allowed_fields=None):
        super(ToDict, self).__init__()
        self.allowed_fields = allowed_fields

        if model_klass:
            self.description = model_descriptions.build_model_to_dict_description(
                model_klass
            )

    def run(self, data, resource, **context):
        resource_model_to_dict = getattr(resource, 'model_to_dict', None)
        overrides = getattr(resource, 'description_overrides', None)
        is_callable = hasattr(resource_model_to_dict, '__call__')

        if resource_model_to_dict and is_callable:
            model_to_dict = resource_model_to_dict
        else:
            model_to_dict = model_descriptions.model_to_dict

        res = list(
            [model_to_dict(model, overrides=overrides) for model in data]
        )
        return {
            'data': res
        }