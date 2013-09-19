from butler.jobs.orm.django.model_descriptions import build_model_to_dict_description


class BaseField(object):

    def contribute_to_class(self, key, klass):
        pass


class RelatedField(BaseField):

    def __init__(self, related_model, allowed_fields=None):
        super(RelatedField, self).__init__()
        self.allowed_fields = allowed_fields
        self.related_model = related_model

    def contribute_to_class(self, key, klass):
        model = klass._meta.model
        if self.allowed_fields:
            description = build_model_to_dict_description(
                klass,
                self.related_model
            )

            keys = set(description.keys())

            for key in keys - set(self.allowed_fields):
                description.pop(key)

            klass.description_overrides = {
                (model, self.related_model): description
            }