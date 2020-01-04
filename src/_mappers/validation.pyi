from typing import Dict
from typing import Union

from _mappers.entities import _EntityFields
from _mappers.mapper import _Config
from _mappers.mapper import _ConfigValue
from _mappers.mapper import _Mapper
from _mappers.mapper import _RelatedField
from _mappers.mapper import Evaluated
from _mappers.sources import _DataSource
from _mappers.sources import _DataSourceFields
from _mappers.sources import _FieldDef

_Mapping = Dict[str, Union[str, _Mapper, Evaluated, _RelatedField]]

def _validate(
    entity_fields: _EntityFields,
    data_source_fields: _DataSourceFields,
    config: _Config,
    data_source: _DataSource,
) -> _Mapping: ...
def _config_types(config: _Config) -> None: ...
def _config_key_type(key: str) -> None: ...
def _config_value_type(value: _ConfigValue) -> None: ...
def _related_field_type(value: _RelatedField) -> None: ...
def _unknown_entity_fields_in_config(
    entity_fields: _EntityFields, config: _Config
) -> None: ...
def _unknown_data_source_fields_in_config(
    data_source_fields: _DataSourceFields, config: _Config
) -> None: ...
def _missing_entity_fields(
    entity_fields: _EntityFields,
    data_source_fields: _DataSourceFields,
    config: _Config,
    data_source: _DataSource,
) -> None: ...
def _required_entity_fields(
    entity_fields: _EntityFields, data_source_fields: _DataSourceFields
) -> None: ...
def _nested_entity_data_source_fields(
    entity_fields: _EntityFields, data_source_fields: _DataSourceFields
) -> None: ...
def _nested_entity_config_fields(
    entity_fields: _EntityFields, config: _Config
) -> None: ...
def _related_config_fields(
    data_source_fields: _DataSourceFields, config: _Config
) -> None: ...
def _related_field_link(value: _FieldDef) -> None: ...
def _get_mapping(
    entity_fields: _EntityFields, data_source_fields: _DataSourceFields, config: _Config
) -> _Mapping: ...
