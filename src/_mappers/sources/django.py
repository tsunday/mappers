from __future__ import absolute_import

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
    for field, field_type in fields.items():
        target_field = config.get(field, field)
        if isinstance(target_field, Evaluated):
            pass
        elif isinstance(target_field, LazyMapper):
            mapper = validate_mapper_field(field, field_type, target_field, data_source)
            config[field] = mapper
        elif isinstance(target_field, str):
            validate_field(target_field, data_source)
        elif isinstance(target_field, tuple):
            assert len(target_field) > 1
            assert all(isinstance(path_field, str) for path_field in target_field)
            model = data_source
            for path_field in target_field[:-1]:
                model_fields = model._meta.get_fields()
                for model_field in model_fields:
                    if model_field.name == path_field:
                        assert model_field.is_relation
                        assert isinstance(
                            getattr(model_field, "attname", object()), str
                        )
                        model = model_field.related_model
                        break
                else:
                    raise Exception(
                        "Can not find '%s' field in the %s model" % (field, model)
                    )
            validate_field(target_field[-1], model)
        else:
            raise Exception(
                "Unknown config value %s in the '%s' field" % (target_field, field)
            )


def validate_field(field, data_source):
    model_fields = data_source._meta.get_fields()
    for model_field in model_fields:
        if field == model_field.name:
            break
        elif model_field.is_relation and field == getattr(
            model_field, "attname", object()
        ):
            break
    else:
        raise Exception(
            "Can not find '%s' field in the %s model" % (field, data_source)
        )


def validate_mapper_field(field, field_type, lazy_mapper, data_source):
    model_fields = data_source._meta.get_fields()
    for model_field in model_fields:
        if model_field.name == field:
            assert model_field.is_relation
            assert isinstance(getattr(model_field, "attname", object()), str)
            mapper = lazy_mapper.build(field_type, model_field.related_model)
            return mapper
    else:
        raise Exception(
            "Can not find '%s' field in the %s model" % (field, data_source)
        )


class ValuesList(object):
    def __init__(self, entity_factory, arguments, iterable_class):
        self.entity_factory = entity_factory
        self.arguments = arguments
        self.iterable_class = iterable_class

    def __call__(self, queryset):
        result = queryset.values_list(*self.arguments)
        result._iterable_class = self.iterable_class
        return result


def get_values_list_arguments(fields, config):
    def add(field):
        value = config.get(field, field)
        if isinstance(value, Mapper):
            result.extend(
                field + "__" + argument for argument in value.iterable.arguments
            )
            return
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

    result = []

    for field in fields:
        add(field)

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
    getters = []
    offset = 0
    for field in fields:
        target_field = config.get(field, field)
        if isinstance(target_field, Mapper):
            limit = offset + len(target_field.iterable.arguments)
            nested_factory = target_field.iterable.entity_factory

            def getter(_row, _factory=nested_factory, _offset=offset, _limit=limit):
                return _factory(*(_row[_offset:_limit]))

            getters.append(getter)
            offset = limit
        else:

            def getter(_row, _offset=offset):
                return _row[_offset]

            getters.append(getter)
            offset += 1

    class _ValuesListIterable(ValuesListIterable):
        def __iter__(self):
            for row in super(_ValuesListIterable, self).__iter__():
                yield entity_factory(*(getter(row) for getter in getters))

    return _ValuesListIterable
