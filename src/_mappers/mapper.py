import operator
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    overload,
)

from django.db.models import Model as DjangoModel
from django.db.models import QuerySet
from django.db.models.query import ValuesListIterable

from _mappers.entities import entity_fields_factory
from _mappers.types import (
    Entity,
    EntityDef,
    EntityFactory,
    Field,
    Fields,
    Row,
    TypingDef,
)


class Evaluated(object):
    def __init__(self, name=None):
        # type: (Optional[str]) -> None
        self.name = name


@overload
def mapper_factory(entity, data_source):
    # type: (EntityDef, DataSource) -> Mapper
    pass


@overload
def mapper_factory(config):
    # type: (Config) -> LazyMapper
    pass


@overload
def mapper_factory(entity, data_source, config):
    # type: (EntityDef, DataSource, Config) -> Mapper
    pass


def mapper_factory(  # type: ignore
    entity=None,  # type: Optional[Union[EntityDef, Config]]
    data_source=None,  # type: Optional[DataSource]
    config=None,  # type: Optional[Config]
):
    # type: (...) -> Union[LazyMapper, Mapper]
    entity, data_source, config = decompose(entity, data_source, config)
    if entity and data_source:
        return Mapper(entity, data_source, config)
    else:
        return LazyMapper(config)


class LazyMapper(object):
    def __init__(self, config):
        # type: (Config) -> None
        self.config = config

    def build(self, entity, data_source):
        # type: (EntityDef, DataSource) -> Mapper
        return Mapper(entity, data_source, self.config)


class Mapper(object):
    values_list_arguments = None  # type: Tuple[str, ...]
    values_list_iterable_class = None  # type: Type[ValuesListIterable]
    entity_factory = None  # type: EntityFactory

    def __init__(self, entity, data_source, config):
        # type: (EntityDef, DataSource, Config) -> None
        self.entity = entity
        self.data_source = data_source
        self.config = config
        configure(self)

    @property
    def reader(self):
        # type: () -> ReaderGetter
        return ReaderGetter(self)


def decompose(
    first,  # type: Optional[Union[EntityDef, Config]]
    second,  # type: Optional[DataSource]
    third,  # type: Optional[Config]
):
    # type: (...) -> Tuple[Optional[EntityDef], Optional[DataSource], Config]
    if first is None and second is None and third is None:
        return None, None, {}
    elif isinstance(first, dict):
        return None, None, first
    elif first is not None and is_django_model(second):
        return first, second, third or {}
    else:
        raise Exception


def configure(mapper):
    # type: (Mapper) -> None
    fields, entity_factory = entity_fields_factory(mapper.entity)
    assert is_django_model(mapper.data_source)
    assert isinstance(mapper.config, dict)
    validate_fields(fields, mapper.data_source, mapper.config)
    mapper.values_list_arguments = get_values_list_arguments(fields, mapper.config)
    mapper.values_list_iterable_class = get_values_list_iterable_class(
        entity_factory, fields, mapper.config
    )
    mapper.entity_factory = entity_factory


class ReaderGetter(object):
    def __init__(self, mapper):
        # type: (Mapper) -> None
        self.mapper = mapper
        self.ret = None  # type: Optional[TypingDef]

    def __call__(self, f):
        # type: (Callable[..., QuerySet]) -> Reader
        if self.ret is None:
            self.ret = f.__annotations__["return"]
        return Reader(f, self.mapper, self.ret)

    def of(self, ret):
        # type: (TypingDef) -> ReaderGetter
        self.ret = ret
        return self


class Reader(object):
    def __init__(self, f, mapper, ret):
        # type: (Callable[..., QuerySet], Mapper, TypingDef) -> None
        self.f = f
        self.values_list_arguments = mapper.values_list_arguments
        self.values_list_iterable_class = mapper.values_list_iterable_class
        self.converter = get_converter(ret, mapper.entity)

    def __call__(self, *args, **kwargs):
        # type: (*Any, **Any) -> Any
        return self.converter(self.raw(*args, **kwargs))

    def raw(self, *args, **kwargs):
        # type: (*Any, **Any) -> QuerySet
        result = self.f(*args, **kwargs).values_list(*self.values_list_arguments)
        result._iterable_class = self.values_list_iterable_class  # type: ignore
        return result  # type: ignore


def get_converter(ret, entity):
    # type: (TypingDef, EntityDef) -> Callable[[QuerySet], Any]
    if ret is entity:
        return operator.methodcaller("get")
    elif ret == List[entity]:  # type: ignore
        return list
    elif ret == Optional[entity]:
        return operator.methodcaller("first")
    else:
        return lambda x: x


# Django.


def is_django_model(data_source):
    # type: (Any) -> bool
    return issubclass(data_source, DjangoModel)


def validate_fields(fields, data_source, config):
    # type: (Fields, DataSource, Config) -> None
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
                        assert model_field.is_relation  # type: ignore
                        assert isinstance(
                            getattr(model_field, "attname", object()), str
                        )
                        model = model_field.related_model  # type: ignore
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


def validate_field(validation_field, data_source):
    # type: (Any, DataSource) -> None
    model_fields = data_source._meta.get_fields()
    for model_field in model_fields:
        if validation_field == model_field.name:
            break
        elif model_field.is_relation and validation_field == getattr(  # type: ignore
            model_field, "attname", object()
        ):
            break
    else:
        raise Exception(
            "Can not find '%s' field in the %s model" % (validation_field, data_source)
        )


def validate_mapper_field(field, field_type, lazy_mapper, data_source):
    # type: (str, Field, LazyMapper, DataSource) -> Mapper
    model_fields = data_source._meta.get_fields()
    for model_field in model_fields:
        if model_field.name == field:
            assert model_field.is_relation  # type: ignore
            assert isinstance(getattr(model_field, "attname", object()), str)
            mapper = lazy_mapper.build(
                field_type, model_field.related_model  # type: ignore
            )
            return mapper
    else:
        raise Exception(
            "Can not find '%s' field in the %s model" % (field, data_source)
        )


def get_values_list_arguments(fields, config):
    # type: (Fields, Config) -> Tuple[str, ...]
    def add(field):
        # type: (str) -> None
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
        elif isinstance(value, LazyMapper):
            raise RuntimeError
        result.append(value)

    result = []  # type: List[str]

    for field in fields:
        add(field)

    return tuple(result)


def get_values_list_iterable_class(entity_factory, fields, config):
    # type: (EntityFactory, Fields, Config) -> Type[ValuesListIterable]
    if any(isinstance(value, Mapper) for value in config.values()):
        return get_nested_values_list_iterable_class(entity_factory, fields, config)
    else:
        return get_flat_values_list_iterable_class(entity_factory)


def get_flat_values_list_iterable_class(entity_factory):
    # type: (EntityFactory) -> Type[ValuesListIterable]
    class _ValuesListIterable(ValuesListIterable):
        def __iter__(self):
            # type: () -> Iterator[Entity]
            for row in super(_ValuesListIterable, self).__iter__():
                yield entity_factory(*row)

    return _ValuesListIterable


def get_nested_values_list_iterable_class(entity_factory, fields, config):
    # type: (EntityFactory, Fields, Config) -> Type[ValuesListIterable]
    getters = []
    offset = 0
    for field in fields:
        target_field = config.get(field, field)
        if isinstance(target_field, Mapper):
            limit = offset + len(target_field.values_list_arguments)
            nested_factory = target_field.entity_factory

            def getter(_row, _factory=nested_factory, _offset=offset, _limit=limit):
                # type: (Row, EntityFactory, int, int) -> Entity
                return _factory(*(_row[_offset:_limit]))

            getters.append(getter)
            offset = limit
        else:

            def getter(_row, _offset=offset):  # type: ignore
                # type: (Row, int) -> Any
                return _row[_offset]

            getters.append(getter)
            offset += 1

    class _ValuesListIterable(ValuesListIterable):
        def __iter__(self):
            # type: () -> Iterator[Entity]
            for row in super(_ValuesListIterable, self).__iter__():
                yield entity_factory(*(getter(row) for getter in getters))

    return _ValuesListIterable


DataSource = Type[DjangoModel]
Config = Dict[str, Union[str, LazyMapper, Mapper, Evaluated, Tuple[str, ...]]]
