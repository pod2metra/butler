from collections import defaultdict
import operator as op
from django.db.models.fields.related import RelatedField, ManyToManyField
from django import forms

descriptions = defaultdict(dict)


def get_m2m_relation_converter(field_name, key):

    def converter(model):
        res = []
        field_value = converter.getter(model)
        for model in field_value.iterator():
            res.append(model_to_dict(model, key))
        return res

    converter.getter = op.attrgetter(field_name)
    return converter


def get_relation_converter(field_name, key):

    def converter(model):
        field_value = converter.getter(model)
        return model_to_dict(field_value, key)

    converter.getter = op.attrgetter(field_name)
    return converter


def build_model_to_dict_description(klass, related_klass=None):
    if related_klass:
        fields = related_klass._meta.fields
    else:
        fields = klass._meta.fields

    description = descriptions[(klass, related_klass)]

    if description:
        return

    for field in fields:
        name = field.name
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
            description[name] = op.attrgetter(name)


def model_to_dict(model, key=None):
    klass = type(model)
    description = descriptions.get(key or (klass, None))
    if not description:
        return forms.model_to_dict(model)

    res = {}
    for field_name, getter in description.items():
        res[field_name] = getter(model)

    return res
