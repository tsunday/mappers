from typing import Optional
from typing import overload
from typing import Tuple
from typing import Union

from _mappers.entities import _Entity
from _mappers.mapper import _Config
from _mappers.mapper import _LazyMapper
from _mappers.mapper import _Mapper
from _mappers.sources import _DataSource
from _mappers.sources.django import _ValuesList
@overload
def mapper_factory() -> _LazyMapper: ...
@overload
def mapper_factory(entity: _Entity, data_source: _DataSource) -> _Mapper: ...
@overload
def mapper_factory(config: _Config) -> _LazyMapper: ...
@overload
def mapper_factory(
    entity: _Entity, data_source: _DataSource, config: _Config
) -> _Mapper: ...
def _decompose(
    *args: Optional[Union[_Entity, _DataSource, _Config]]
) -> Tuple[Optional[_Entity], Optional[_DataSource], _Config]: ...
def _no_arguments() -> Tuple[None, None, _Config]: ...
def _config_only(config: _Config) -> Tuple[None, None, _Config]: ...
def _entity_and_data_source(
    entity: _Entity, data_source: _DataSource
) -> Tuple[_Entity, _DataSource, _Config]: ...
def _everything(
    entity: _Entity, data_source: _DataSource, config: _Config
) -> Tuple[_Entity, _DataSource, _Config]: ...
def _configure(
    entity: _Entity, data_source: _DataSource, config: _Config
) -> _ValuesList: ...
