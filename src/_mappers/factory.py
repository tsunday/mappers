from _mappers.entities import entity_fields_factory
from _mappers.mapper import LazyMapper
from _mappers.mapper import Mapper
from _mappers.sources import data_source_factory


def mapper_factory(entity=None, data_source=None, config=None):
    entity, data_source, config = decompose(entity, data_source, config)
    assert isinstance(config, dict)
    if entity and data_source:
        iterable = configure(entity, data_source, config)
        return Mapper(entity, data_source, config, iterable)
    else:
        return LazyMapper(config)


def decompose(first, second, third):
    if first is None and second is None and third is None:
        return None, None, {}
    elif isinstance(first, dict) and second is None and third is None:
        return None, None, first
    elif first is not None and second is not None:
        return first, second, third or {}
    else:
        raise Exception


def configure(entity, data_source, config):
    fields, entity_factory = entity_fields_factory(entity)
    iterable = data_source_factory(fields, entity_factory, data_source, config)
    return iterable
