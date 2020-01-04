from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type

from django.db.models import Field
from django.db.models import Model
from django.db.models import QuerySet
from django.db.models.query import ValuesListIterable
from django.db.models.query import ValuesQuerySet

from _mappers.entities import _EntityFactory
from _mappers.entities import _EntityFields
from _mappers.mapper import _Mapper
from _mappers.mapper import _RelatedField
from _mappers.mapper import Evaluated
from _mappers.sources import _DataSourceFields
from _mappers.sources import _FieldDef
from _mappers.sources import _FieldName
from _mappers.validation import _Mapping

_DjangoModel = Type[Model]
_ValuesListIterable = Type[ValuesListIterable]

def _is_django_model(data_source: Any) -> bool: ...
def _get_fields(
    data_source: _DjangoModel, exclude: Optional[Field] = ...
) -> _DataSourceFields: ...
def _get_field_names(field: Field) -> Iterable[_FieldName]: ...
def _disassemble_field(field: Field) -> _FieldDef: ...
def _factory(
    fields: _EntityFields, entity_factory: _EntityFactory, mapping: _Mapping
) -> _ValuesList: ...

class _ValuesList:
    def __init__(
        self,
        fields: _EntityFields,
        entity_factory: _EntityFactory,
        mapping: _Mapping,
        arguments: Tuple[str, ...],
        iterable_class: _ValuesListIterable,
    ) -> None: ...
    def __call__(self, queryset: QuerySet) -> ValuesQuerySet: ...

def _get_values_list_arguments(
    fields: _EntityFields, mapping: _Mapping
) -> Tuple[str, ...]: ...
def _build_mapper_argument(field: str, value: _Mapper) -> List[str]: ...
def _build_evaluated_argument(field: str, value: Evaluated) -> List[str]: ...
def _build_related_argument(field: str, value: _RelatedField) -> List[str]: ...
def _build_field_argument(field: str, value: str) -> List[str]: ...
def _get_values_list_iterable_class(
    entity_factory: _EntityFactory, fields: _EntityFields, mapping: _Mapping
) -> _ValuesListIterable: ...
def _get_flat_values_list_iterable_class(
    entity_factory: _EntityFactory,
) -> _ValuesListIterable: ...
def _get_nested_values_list_iterable_class(
    entity_factory: _EntityFactory, fields: _EntityFields, mapping: _Mapping
) -> _ValuesListIterable: ...
def _build_field_getter(offset: int) -> Callable: ...
def _build_entity_getter(
    entity_factory: _EntityFactory,
    fields: _EntityFields,
    mapping: _Mapping,
    offset: int,
) -> Callable: ...
