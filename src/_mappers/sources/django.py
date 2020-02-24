# -*- coding: utf-8 -*-
from __future__ import absolute_import

import inspect

from _mappers.mapper import _Mapper
from _mappers.mapper import Evaluated

try:
    from django.db.models import Model as DjangoModel
    from django.db.models.query import ValuesListIterable

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def _is_django_model(data_source):
    if IS_AVAILABLE:
        return inspect.isclass(data_source) and issubclass(data_source, DjangoModel)
    else:
        return False


def _get_fields(data_source, exclude=None):
    fields = {}
    for field in data_source._meta._get_fields():
        if field is exclude:
            continue
        names = _get_field_names(field)
        disassembled = _disassemble_field(field)
        for name in names:
            fields[name] = disassembled
    return fields


def _get_field_names(field):
    yield field.name
    attname = getattr(field, "attname", None)
    if attname is not None and field.name != attname:
        yield attname


def _disassemble_field(field):
    disassembled = {
        "is_nullable": bool(field.null),
        "is_link": field.is_relation,
        "is_collection": field.many_to_many,
    }
    if disassembled["is_link"] and not disassembled["is_collection"]:
        disassembled["link"] = field.related_model
        disassembled["link_to"] = _get_fields(
            field.related_model, exclude=field.remote_field
        )
    return disassembled


def _factory(fields, entity_factory, mapping):
    return _ValuesList(
        fields,
        entity_factory,
        mapping,
        _get_values_list_arguments(fields, mapping),
        _get_values_list_iterable_class(entity_factory, fields, mapping),
    )


class _ValuesList(object):
    def __init__(self, fields, entity_factory, mapping, arguments, iterable_class):
        self.fields = fields
        self.entity_factory = entity_factory
        self.mapping = mapping
        self.arguments = arguments
        self.iterable_class = iterable_class

    def __call__(self, queryset):
        result = queryset.values_list(*self.arguments)
        result._iterable_class = self.iterable_class
        return result


def _get_values_list_arguments(fields, mapping):
    result = []
    for field, _field_type in fields:
        result.extend(builders[type(mapping[field])](field, mapping[field]))
    return tuple(result)


def _build_mapper_argument(field, value):
    return [field + "__" + argument for argument in value.iterable.arguments]


def _build_evaluated_argument(field, value):
    return [value.name or field]


def _build_related_argument(field, value):
    return ["__".join(value)]


def _build_field_argument(field, value):
    return [value]


builders = {
    _Mapper: _build_mapper_argument,
    Evaluated: _build_evaluated_argument,
    tuple: _build_related_argument,
    str: _build_field_argument,
}


def _get_values_list_iterable_class(entity_factory, fields, mapping):
    if any(isinstance(value, _Mapper) for value in mapping.values()):
        return _get_nested_values_list_iterable_class(entity_factory, fields, mapping)
    else:
        return _get_flat_values_list_iterable_class(entity_factory)


def _get_flat_values_list_iterable_class(entity_factory):
    class _ValuesListIterable(ValuesListIterable):
        def __iter__(self):
            for row in super(_ValuesListIterable, self).__iter__():
                yield entity_factory(*row)

    return _ValuesListIterable


def _get_nested_values_list_iterable_class(entity_factory, fields, mapping):
    getter, _offset = _build_entity_getter(entity_factory, fields, mapping, 0)

    class _ValuesListIterable(ValuesListIterable):
        def __iter__(self):
            for row in super(_ValuesListIterable, self).__iter__():
                yield getter(row)

    return _ValuesListIterable


def _build_field_getter(offset):
    def getter(row):
        return row[offset]

    return getter, offset + 1


def _build_entity_getter(entity_factory, fields, mapping, offset):
    getters = []

    for field, _field_type in fields:
        target_field = mapping[field]
        if isinstance(target_field, _Mapper):
            getter, offset = _build_entity_getter(
                target_field.iterable.entity_factory,
                target_field.iterable.fields,
                target_field.iterable.mapping,
                offset,
            )
        else:
            getter, offset = _build_field_getter(offset)
        getters.append(getter)

    def getter(row):
        return entity_factory(*(getter(row) for getter in getters))

    return getter, offset
