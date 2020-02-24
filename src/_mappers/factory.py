# -*- coding: utf-8 -*-
from _mappers.entities import _entity_factory
from _mappers.exceptions import MapperError
from _mappers.mapper import _LazyMapper
from _mappers.mapper import _Mapper
from _mappers.sources import _data_source_factory
from _mappers.validation import _validate


def mapper_factory(entity=None, data_source=None, config=None):
    """Define declarative mapper from data source to domain entity."""
    entity, data_source, config = _decompose(entity, data_source, config)
    if not isinstance(config, dict):
        raise MapperError
    if entity and data_source:
        iterable = _configure(entity, data_source, config)
        return _Mapper(entity, data_source, config, iterable)
    else:
        return _LazyMapper(config)


def _decompose(*args):
    args = tuple(filter(None, args))
    return arguments[len(args)](*args)


def _no_arguments():
    return None, None, {}


def _config_only(config):
    return None, None, config


def _entity_and_data_source(entity, data_source):
    return entity, data_source, {}


def _everything(entity, data_source, config):
    return entity, data_source, config


arguments = {
    0: _no_arguments,
    1: _config_only,
    2: _entity_and_data_source,
    3: _everything,
}


def _configure(entity, data_source, config):
    fields, entity_factory = _entity_factory(entity)
    data_source_fields, data_source_factory = _data_source_factory(data_source)
    mapping = _validate(dict(fields), data_source_fields, config, data_source)
    iterable = data_source_factory(fields, entity_factory, mapping)
    return iterable
