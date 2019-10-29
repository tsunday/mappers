from typing import _SpecialForm as TypingDef
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import overload
from typing import Tuple
from typing import Type
from typing import Union

from django.db.models import Model as DjangoModel
from django.db.models import QuerySet
from django.db.models.query import ValuesListIterable
from typing_extensions import Protocol

DataSource = Type[DjangoModel]

Config = Dict[str, Union[str, LazyMapper, Mapper, Evaluated, Tuple[str, ...]]]

Entity = Any

EntityDef = Type[Entity]

Field = Type[Any]

Fields = Dict[str, Field]

Row = Tuple[Any, ...]

class EntityFactory(Protocol):
    def __call__(self, *row: Any) -> Entity: ...

class Evaluated:
    def __init__(self, name: Optional[str] = ...) -> None: ...

@overload
def mapper_factory(entity: EntityDef, data_source: DataSource) -> Mapper: ...
@overload
def mapper_factory(config: Config) -> LazyMapper: ...
@overload
def mapper_factory(
    entity: EntityDef, data_source: DataSource, config: Config
) -> Mapper: ...

class LazyMapper:
    def __init__(self, config: Config) -> None: ...
    def build(self, entity: EntityDef, data_source: DataSource) -> Mapper: ...

class Mapper:
    values_list_arguments: Tuple[str, ...]
    values_list_iterable_class: Type[ValuesListIterable]
    entity_factory: EntityFactory
    def __init__(
        self, entity: EntityDef, data_source: DataSource, config: Config
    ) -> None: ...
    reader: ReaderGetter

def decompose(
    first: Optional[Union[EntityDef, Config]],
    second: Optional[DataSource],
    third: Optional[Config],
) -> Tuple[Optional[EntityDef], Optional[DataSource], Config]: ...
def configure(mapper: Mapper) -> None: ...

class ReaderGetter:
    mapper: Mapper
    ret: Optional[TypingDef]
    def __init__(self, mapper: Mapper) -> None: ...
    def __call__(self, f: Callable[..., QuerySet]) -> Reader: ...
    def of(self, ret: TypingDef) -> ReaderGetter: ...

class Reader:
    def __init__(
        self, f: Callable[..., QuerySet], mapper: Mapper, ret: TypingDef
    ) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    def raw(self, *args: Any, **kwargs: Any) -> QuerySet: ...

def get_converter(ret: TypingDef, entity: EntityDef) -> Callable[[QuerySet], Any]: ...
def is_django_model(data_source: Any) -> bool: ...
def validate_fields(
    fields: Fields, data_source: DataSource, config: Config
) -> None: ...
def validate_field(validation_field: str, data_source: DataSource) -> None: ...
def validate_mapper_field(
    field: str, field_type: Field, lazy_mapper: LazyMapper, data_source: DataSource
) -> Mapper: ...
def get_values_list_arguments(fields: Fields, config: Config) -> Tuple[str, ...]: ...
def get_values_list_iterable_class(
    entity_factory: EntityFactory, fields: Fields, config: Config
) -> Type[ValuesListIterable]: ...
def get_flat_values_list_iterable_class(
    entity_factory: EntityFactory,
) -> Type[ValuesListIterable]: ...
def get_nested_values_list_iterable_class(
    entity_factory: EntityFactory, fields: Fields, config: Config
) -> Type[ValuesListIterable]: ...
