from _mappers.entities import _EntityFactory
from _mappers.entities import _Fields
from _mappers.mapper import _Config
from _mappers.sources.django import _DjangoModel
from _mappers.sources.django import ValuesList

_DataSource = _DjangoModel

def data_source_factory(
    fields: _Fields,
    entity_factory: _EntityFactory,
    data_source: _DataSource,
    config: _Config,
) -> ValuesList: ...
