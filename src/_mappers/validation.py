# -*- coding: utf-8 -*-
from _mappers.exceptions import MapperError
from _mappers.mapper import _LazyMapper
from _mappers.mapper import Evaluated


def _validate(entity_fields, data_source_fields, config, data_source):
    _config_types(config)
    _unknown_entity_fields_in_config(entity_fields, config)
    _unknown_data_source_fields_in_config(data_source_fields, config)
    _missing_entity_fields(entity_fields, data_source_fields, config, data_source)
    _required_entity_fields(entity_fields, data_source_fields)
    _nested_entity_data_source_fields(entity_fields, data_source_fields)
    _nested_entity_config_fields(entity_fields, config)
    _related_config_fields(data_source_fields, config)
    return _get_mapping(entity_fields, data_source_fields, config)


def _config_types(config):
    for key, value in config.items():
        _config_key_type(key)
        _config_value_type(value)


def _config_key_type(key):
    if not isinstance(key, str):
        raise MapperError


def _config_value_type(value):
    if isinstance(value, (_LazyMapper, Evaluated, str)):
        pass
    elif isinstance(value, tuple):
        _related_field_type(value)
    else:
        raise MapperError


def _related_field_type(value):
    if len(value) < 2:
        raise MapperError
    elif any(not isinstance(v, str) for v in value):
        raise MapperError


def _unknown_entity_fields_in_config(entity_fields, config):
    if set(config) - set(entity_fields):
        raise MapperError


def _unknown_data_source_fields_in_config(data_source_fields, config):
    values = (value for value in config.values() if isinstance(value, str))
    if set(values) - set(data_source_fields):
        raise MapperError


def _missing_entity_fields(entity_fields, data_source_fields, config, data_source):
    missing = set(entity_fields) - (set(data_source_fields) | set(config))
    if missing:
        raise MapperError(
            "Can not find {!r} field in the {!r} model".format(
                next(iter(missing)), data_source,
            )
        )


def _required_entity_fields(entity_fields, data_source_fields):
    for field_name in set(entity_fields) & set(data_source_fields):
        if (
            not entity_fields[field_name]["is_optional"]
            and data_source_fields[field_name]["is_nullable"]
        ):
            raise MapperError


def _nested_entity_data_source_fields(entity_fields, data_source_fields):
    for field_name in set(entity_fields) & set(data_source_fields):
        if (
            entity_fields[field_name]["is_entity"]
            and data_source_fields[field_name]["is_collection"]
        ):
            raise MapperError


def _nested_entity_config_fields(entity_fields, config):
    for field_name in set(entity_fields) & set(config):
        if entity_fields[field_name]["is_entity"] and not isinstance(
            config[field_name], _LazyMapper
        ):
            raise MapperError


def _related_config_fields(data_source_fields, config):
    link_to = data_source_fields
    for value in config.values():
        if isinstance(value, tuple):
            for related in value[:-1]:
                _related_field_link(link_to[related])
                link_to = link_to[related]["link_to"]


def _related_field_link(value):
    if not value["is_link"]:
        raise MapperError
    if value["is_collection"]:
        raise MapperError


def _get_mapping(entity_fields, data_source_fields, config):
    from _mappers.factory import mapper_factory

    mapping = {}
    for field, field_type in entity_fields.items():
        if field_type["is_entity"]:
            mapping[field] = mapper_factory(
                field_type["type"],
                data_source_fields[field]["link"],
                config.get(field, mapper_factory()).config,
            )
        else:
            mapping[field] = config.get(field, field)
    return mapping
