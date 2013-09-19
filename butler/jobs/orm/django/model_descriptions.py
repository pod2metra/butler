from collections import defaultdict
import operator as op
from django.db.models.fields.related import RelatedField, ManyToManyField
from django import forms


descriptions = defaultdict(dict)


def get_m2m_relation_converter(field_name, key):

    def converter(model, overrides=None):
        res = []
        field_value = converter.getter(model)
        for model in field_value.iterator():
            res.append(model_to_dict(model, key, overrides=overrides))
        return res

    converter.getter = op.attrgetter(field_name)
    return converter


def get_relation_converter(field_name, key):

    def converter(model, overrides=None):
        field_value = converter.getter(model)
        return model_to_dict(field_value, key, overrides=overrides)

    converter.getter = op.attrgetter(field_name)
    return converter


def get_simple_converter(field_name):
    getter = op.attrgetter(field_name)

    def converter(model, overrides=None):
        return getter(model)

    return converter


def build_model_to_dict_description(klass, related_klass=None, allowed_fields=None):
    if related_klass:
        fields = related_klass._meta.fields
    else:
        fields = klass._meta.fields

    description = descriptions[(klass, related_klass)]

    if description:
        return description

    for field in fields:
        name = field.name

        if allowed_fields and name not in allowed_fields:
            continue

        field_class = type(field)
        if issubclass(field_class, RelatedField):
            build_model_to_dict_description(klass, field.rel.to)
            description_key = (klass, field.rel.to,)
            if issubclass(field_class, ManyToManyField):
                description[name] = get_m2m_relation_converter(
                    name,
                    description_key
                )
            else:
                description[name] = get_relation_converter(
                    name,
                    description_key
                )
        else:
            description[name] = get_simple_converter(
                name
            )

    return description


def model_to_dict(model, key=None, overrides=None):
    klass = type(model)

    description = overrides and overrides.get(key or (klass, None))
    if not description:
        description = descriptions.get(key or (klass, None))

    if not description:
        return forms.model_to_dict(model)

    res = {}
    for field_name, getter in description.items():
        res[field_name] = getter(model, overrides)

    return res
