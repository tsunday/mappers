from typing import Any
from typing import Tuple
from typing import Type

from django.db.models import Model
from django.db.models import QuerySet
from django.db.models.query import ValuesListIterable
from django.db.models.query import ValuesQuerySet

from _mappers.entities import _EntityFactory
from _mappers.entities import _Field
from _mappers.entities import _Fields
from _mappers.mapper import _Config
from _mappers.mapper import LazyMapper
from _mappers.mapper import Mapper

_DjangoModel = Type[Model]
_ValuesListIterable = Type[ValuesListIterable]

def is_django_model(data_source: Any) -> bool: ...
def validate_fields(
    fields: _Fields, data_source: _DjangoModel, config: _Config
) -> None: ...
def validate_field(field: str, data_source: _DjangoModel) -> None: ...
def validate_mapper_field(
    field: str, field_type: _Field, lazy_mapper: LazyMapper, data_source: _DjangoModel,
) -> Mapper: ...

class ValuesList:
    def __init__(
        self,
        entity_factory: _EntityFactory,
        arguments: Tuple[str, ...],
        iterable_class: _ValuesListIterable,
    ) -> None: ...
    def __call__(self, queryset: QuerySet) -> ValuesQuerySet: ...

def get_values_list_arguments(fields: _Fields, config: _Config) -> Tuple[str, ...]: ...
def get_values_list_iterable_class(
    entity_factory: _EntityFactory, fields: _Fields, config: _Config
) -> _ValuesListIterable: ...
def get_flat_values_list_iterable_class(
    entity_factory: _EntityFactory,
) -> _ValuesListIterable: ...
def get_nested_values_list_iterable_class(
    entity_factory: _EntityFactory, fields: _Fields, config: _Config
) -> _ValuesListIterable: ...
