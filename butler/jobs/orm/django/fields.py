from django.db.models.fields import related
from butler.jobs.orm.django.model_descriptions import \
    build_model_to_dict_description, get_relation_converter, \
    get_m2m_relation_converter, get_simple_converter


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

        description = build_model_to_dict_description(
            klass,
            self.related_model
        )

        keys = set(description.keys())

        for key in keys - set(self.allowed_fields or []):
            description.pop(key)

        klass.description_overrides = {
            (model, self.related_model): description
        }


class PropertyField(BaseField):
    def contribute_to_class(self, key, klass):
        model = klass._meta.model
        description_key = (model, None)
        description = build_model_to_dict_description(
            *description_key
        )

        value = getattr(model, key, None)

        if issubclass(type(value), related.SingleRelatedObjectDescriptor):
            converter = get_relation_converter(
                key,
                (value.related.model, None)
            )
        elif issubclass(type(value), related.ForeignRelatedObjectsDescriptor):
            converter = get_m2m_relation_converter(
                key,
                (value.related.model, None)
            )
        else:
            converter = get_simple_converter(key)

        description[key] = converter



