from __future__ import absolute_import

from _mappers.compat import is_optional
from _mappers.entities import is_entity
from _mappers.exceptions import MapperError
from _mappers.mapper import Evaluated
from _mappers.mapper import LazyMapper
from _mappers.mapper import Mapper

try:
    from django.db.models import Model as DjangoModel
    from django.db.models.query import ValuesListIterable

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def is_django_model(data_source):
    if IS_AVAILABLE:
        return issubclass(data_source, DjangoModel)
    else:
        return False


def validate_fields(fields, data_source, config):
    for field, field_type in fields:
        target_field = config.get(field, field)
        if isinstance(target_field, Evaluated):
            validate_evaluated_field(field_type)
        elif isinstance(target_field, LazyMapper):
            mapper = validate_mapper_field(field, field_type, target_field, data_source)
            config[field] = mapper
        elif isinstance(target_field, str):
            validate_field(target_field, field_type, data_source)
        elif isinstance(target_field, tuple):
            assert len(target_field) > 1
            assert all(isinstance(path_field, str) for path_field in target_field)
            model = data_source
            for path_field in target_field[:-1]:
                model_field = get_data_source_field(path_field, model)
                assert model_field.is_relation
                assert getattr(model_field, "attname", False)
                model = model_field.related_model
            validate_field(target_field[-1], field_type, model)
        else:
            raise Exception(
                "Unknown config value %s in the '%s' field" % (target_field, field)
            )


def validate_field(field, field_type, data_source):
    validate_evaluated_field(field_type)
    model_field = get_data_source_field(field, data_source)
    if model_field.null is True and not is_optional(field_type):
        raise MapperError


def validate_evaluated_field(field_type):
    if is_entity(field_type):
        raise MapperError


def validate_mapper_field(field, field_type, lazy_mapper, data_source):
    model_field = get_data_source_field(field, data_source)
    assert model_field.is_relation
    assert getattr(model_field, "attname", False)
    mapper = lazy_mapper.build(field_type, model_field.related_model)
    return mapper


def get_data_source_field(name, data_source):
    for field in data_source._meta.get_fields():
        if field.name == name:
            return field
        elif field.is_relation and name == getattr(field, "attname", object()):
            return field
    else:
        raise MapperError(
            "Can not find '%s' field in the %s model" % (name, data_source)
        )


class ValuesList(object):
    def __init__(self, fields, entity_factory, arguments, iterable_class):
        self.fields = fields
        self.entity_factory = entity_factory
        self.arguments = arguments
        self.iterable_class = iterable_class

    def __call__(self, queryset):
        result = queryset.values_list(*self.arguments)
        result._iterable_class = self.iterable_class
        return result


def get_values_list_arguments(fields, config):

    result = []

    for field, _field_type in fields:
        value = config.get(field, field)
        if isinstance(value, Mapper):
            result.extend(
                field + "__" + argument for argument in value.iterable.arguments
            )
            continue
        elif isinstance(value, Evaluated):
            if value.name is None:
                value = field
            else:
                value = value.name
        elif isinstance(value, tuple):
            value = "__".join(value)
        elif isinstance(value, LazyMapper):
            raise RuntimeError
        result.append(value)

    return tuple(result)


def get_values_list_iterable_class(entity_factory, fields, config):
    if any(isinstance(value, Mapper) for value in config.values()):
        return get_nested_values_list_iterable_class(entity_factory, fields, config)
    else:
        return get_flat_values_list_iterable_class(entity_factory)


def get_flat_values_list_iterable_class(entity_factory):
    class _ValuesListIterable(ValuesListIterable):
        def __iter__(self):
            for row in super(_ValuesListIterable, self).__iter__():
                yield entity_factory(*row)

    return _ValuesListIterable


def get_nested_values_list_iterable_class(entity_factory, fields, config):
    getter, _offset = build_entity_getter(entity_factory, fields, config, 0)

    class _ValuesListIterable(ValuesListIterable):
        def __iter__(self):
            for row in super(_ValuesListIterable, self).__iter__():
                yield getter(row)

    return _ValuesListIterable


def build_field_getter(offset):
    def getter(row):
        return row[offset]

    return getter, offset + 1


def build_entity_getter(entity_factory, fields, config, offset):
    getters = []

    for field, _field_type in fields:
        target_field = config.get(field, field)
        if isinstance(target_field, Mapper):
            getter, offset = build_entity_getter(
                target_field.iterable.entity_factory,
                target_field.iterable.fields,
                target_field.config,
                offset,
            )
        else:
            getter, offset = build_field_getter(offset)
        getters.append(getter)

    def getter(row):
        return entity_factory(*(getter(row) for getter in getters))

    return getter, offset
