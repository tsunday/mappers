from typing import Optional
from typing import overload
from typing import Tuple
from typing import Type
from typing import TypeVar

from _mappers.mapper import _Config
from _mappers.mapper import LazyMapper
from _mappers.mapper import Mapper
from _mappers.sources import _DataSource
from _mappers.sources.django import ValuesList
@overload
def mapper_factory(entity: Type, data_source: _DataSource) -> Mapper: ...
@overload
def mapper_factory(config: _Config) -> LazyMapper: ...
@overload
def mapper_factory(
    entity: Type, data_source: _DataSource, config: _Config
) -> Mapper: ...

_T = TypeVar("_T")
@overload
def decompose(
    first: None, second: None, third: None,
) -> Tuple[None, None, _Config]: ...
@overload
def decompose(
    first: _Config, second: None, third: None,
) -> Tuple[None, None, _Config]: ...
@overload
def decompose(
    first: _T, second: _DataSource, third: Optional[_Config],
) -> Tuple[_T, _DataSource, _Config]: ...
def configure(
    entity: Type, data_source: _DataSource, config: _Config
) -> ValuesList: ...
