from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Tuple

from typing_extensions import TypedDict

from _mappers.entities import _EntityFactory
from _mappers.entities import _EntityFields
from _mappers.sources.django import _DjangoModel
from _mappers.sources.django import _ValuesList
from _mappers.validation import _Mapping

_FieldName = str

class _FieldDef(TypedDict):
    is_nullable: bool
    is_link: bool
    is_collection: bool
    link: Optional[_DjangoModel]
    link_to: Any  # A recursive type actually.

_DataSourceFields = Dict[_FieldName, _FieldDef]

_DataSource = _DjangoModel

_DataSourceFactory = Callable[[_EntityFields, _EntityFactory, _Mapping], _ValuesList]

def _data_source_factory(
    data_source: _DataSource,
) -> Tuple[_DataSourceFields, _DataSourceFactory]: ...
