"""
mappers
-------

This module implements Declarative mappers from ORM models to domain entities.

:copyright: (c) 2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""

import dataclasses
import operator
import typing

from django.db.models import Model as DjangoModel
from django.db.models.query import ValuesListIterable


# TODO:
#
# [ ] Converter from typing.  This code should return a list of
#     `Channel` instances.
#
#     channel_mapper = Mapper(Channel, models.Channel, {"primary_key": "pk"})
#
#     @channel_mapper.reader
#     def load_channels(user: User) -> List[Channel]:
#         pass
#
# [ ] Raw data source access.  This code should return `QuerySet`
#     iterating over `Channel` instances.
#
#     load_channels.raw(User(primary_key=1))
#
# [ ] Field not found in the data source.  This code should not found
#     `community_id` field.
#
#     mapper = Mapper(Message, models.Message, {"primary_key": "pk"})
#
# [ ] Related user expand.  This code should return a list of
#     `Message` dataclass instances.  Each `Message` instance have
#     nested instance of the `User` dataclass.
#
#     mapper = Mapper(
#         Message,
#         models.Message,
#         {"user": Mapper({"primary_key": "id"})},
#     )
#
#     @mapper.reader
#     def list_for_user(user: User, channel_id: ChannelId) -> List[Message]:
#         pass
#
# [ ] Validate mapped fields.  This code below should fail with error.
#
#     class OrderModel(db.Model):
#         total = db.IntegerField(null=True)
#
#     @dataclass
#     class Order:
#         total: int
#
# [ ] Validate mapper related fields.  We can't expand `User` if
#     related field is not ForeignKey.
#
# [ ] Validate related fields config.  We can't expand `User` if
#     passed configuration isn't a `Mapper` instance.
#
# [ ] Resolve community_id without config entry from `community`
#     foreign key field on the `Channel` model.
#
# [ ] Tuple target field configuration.  This code should resolve to
#     the `community_id` field in the `Channel` model of the `Message`
#     model.
#
#     mapper = Mapper(
#         Message, models.Message, {"community_id": ("channel", "community_id")}
#     )
#
#     @mapper.reader
#     def list_for_user(user: User, channel_id: ChannelId) -> List[Message]:
#         pass
#
# [ ] Support evaluated name argument.  Code below should require
#     `user_random_id` annotation on queryset and pass it to the
#     `random_id` dataclass argument.
#
#     mapper = Mapper(
#         Message, models.Message, {"random_id": Evaluated("user_random_id")}
#     )
#
#     @mapper.reader
#     def list_for_user(user: User, channel_id: ChannelId) -> List[Message]:
#         pass
#
# [ ] Map to the optional single object.  This code below should call
#     `first` method of the returned queryset.
#
#     @mapper.reader
#     def load_user(primary_key: UserId) -> Optional[User]:
#         return models.User.objects.filter(pk=primary_key)
#
# [ ] Map to the required single object.  This code below should call
#     `get` method of the returned queryset.
#
#     @mapper.reader
#     def load_user(primary_key: UserId) -> User:
#         return models.User.objects.filter(pk=primary_key)


class Evaluated(object):
    def __init__(self, name=None):
        self.name = name


class Mapper(object):
    def __init__(self, *args):
        entity, data_source, config = decompose(args)
        self.entity = entity
        self.data_source = data_source
        self.config = config
        if entity:
            configure(self)

    def reader(self, f):
        return Reader(f, self)


def decompose(args):
    length = len(args)
    if length == 0:
        return None, None, {}
    elif length == 1:
        return None, None, args[0]
    elif length == 2:
        return args[0], args[1], {}
    elif length == 3:
        return args
    else:
        raise Exception


def configure(mapper):
    assert is_dataclass(mapper.entity)
    assert is_django_model(mapper.data_source)
    assert isinstance(mapper.config, dict)
    fields = get_fields(mapper.entity)
    validate_fields(fields, mapper.data_source, mapper.config)
    mapper.values_list_arguments = get_values_list_arguments(fields, mapper.config)
    mapper.values_list_iterable_class = get_values_list_iterable_class(
        mapper.entity, fields, mapper.config
    )


class Reader(object):
    def __init__(self, f, mapper):
        self.f = f
        self.values_list_arguments = mapper.values_list_arguments
        self.values_list_iterable_class = mapper.values_list_iterable_class
        self.converter = get_converter(f, mapper)

    def __call__(self, *args, **kwargs):
        return self.converter(self.raw(*args, **kwargs))

    def raw(self, *args, **kwargs):
        result = self.f(*args, **kwargs)
        result = result.values_list(*self.values_list_arguments)
        result._iterable_class = self.values_list_iterable_class
        return result


def get_converter(f, mapper):
    ret = f.__annotations__["return"]
    if ret is mapper.entity:
        # -> Entity
        return operator.methodcaller("get")
    elif isinstance(ret, typing._GenericAlias):
        if (
            isinstance(ret.__origin__, typing._SpecialForm)
            and ret.__origin__._name == "Union"
            and ret.__args__ == (mapper.entity, type(None))
        ):
            # -> Optional[Entity]
            return operator.methodcaller("first")
        else:
            # -> List[Entity]
            return ret.__origin__
    else:
        # -> ???
        return lambda x: x


# Dataclasses.


def is_dataclass(entity):
    return (
        getattr(entity, dataclasses._FIELDS, None) is not None
        and getattr(entity, dataclasses._PARAMS, None) is not None
    )


def get_fields(entity):
    return dict(
        (name, field.type)
        for name, field in getattr(entity, dataclasses._FIELDS).items()
    )


# Django.


def is_django_model(data_source):
    return issubclass(data_source, DjangoModel)


def validate_fields(fields, data_source, config):
    for field, field_type in fields.items():
        target_field = config.get(field, field)
        if isinstance(target_field, Evaluated):
            pass
        elif isinstance(target_field, Mapper):
            validate_mapper_field(field, field_type, target_field, data_source)
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
                        f"Can not fiend '{field}' field in the {model} model"
                    )
            validate_field(target_field[-1], model)
        else:
            raise Exception(
                f"Unknown config value {target_field} in the '{field}' field"
            )


def validate_field(validation_field, data_source):
    model_fields = data_source._meta.get_fields()
    for model_field in model_fields:
        if validation_field == model_field.name:
            break
        elif model_field.is_relation and validation_field == getattr(
            model_field, "attname", object()
        ):
            break
    else:
        raise Exception(
            f"Can not fiend '{validation_field}' field in the {data_source} model"
        )


def validate_mapper_field(field, field_type, mapper, data_source):
    assert mapper.entity is None
    assert mapper.data_source is None
    model_fields = data_source._meta.get_fields()
    for model_field in model_fields:
        if model_field.name == field:
            assert model_field.is_relation
            assert isinstance(getattr(model_field, "attname", object()), str)
            mapper.entity = field_type
            mapper.data_source = model_field.related_model
            configure(mapper)
            break
    else:
        raise Exception(f"Can not fiend '{field}' field in the {data_source} model")


def get_values_list_arguments(fields, config):
    def add(field, config):
        value = config.get(field, field)
        if isinstance(value, Mapper):
            result.extend(
                field + "__" + argument for argument in value.values_list_arguments
            )
            return
        elif isinstance(value, Evaluated):
            if value.name is None:
                value = field
            else:
                value = value.name
        elif isinstance(value, tuple):
            value = "__".join(value)
        result.append(value)

    result = []

    for field in fields:
        add(field, config)

    return tuple(result)


def get_values_list_iterable_class(entity, fields, config):
    if any(isinstance(value, Mapper) for value in config.values()):
        return get_nested_values_list_iterable_class(entity, fields, config)
    else:
        return get_flat_values_list_iterable_class(entity)


def get_flat_values_list_iterable_class(entity):
    class _ValuesListIterable(ValuesListIterable):
        def __iter__(self):
            for row in super().__iter__():
                yield entity(*row)

    return _ValuesListIterable


def get_nested_values_list_iterable_class(entity, fields, config):
    getters = []
    offset = 0
    for field in fields:
        target_field = config.get(field, field)
        if isinstance(target_field, Mapper):
            limit = offset + len(target_field.values_list_arguments)

            def getter(_row, _entity=target_field.entity, _offset=offset, _limit=limit):
                return _entity(*(_row[_offset:_limit]))

            getters.append(getter)
            offset = limit
        else:

            def getter(_row, _offset=offset):
                return _row[_offset]

            getters.append(getter)
            offset += 1

    class _ValuesListIterable(ValuesListIterable):
        def __iter__(self):
            for row in super().__iter__():
                yield entity(*(getter(row) for getter in getters))

    return _ValuesListIterable
