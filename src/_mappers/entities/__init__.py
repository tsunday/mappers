from _mappers.entities import attrs
from _mappers.entities import dataclasses
from _mappers.entities import pydantic


def is_entity(entity):
    return (
        attrs.is_attrs(entity)
        or dataclasses.is_dataclass(entity)
        or pydantic.is_pydantic(entity)
    )


def entity_fields_factory(entity):
    if attrs.is_attrs(entity):
        fields = attrs.get_fields(entity)
        factory = attrs.get_factory(fields, entity)
        return fields, factory
    elif dataclasses.is_dataclass(entity):
        fields = dataclasses.get_fields(entity)
        factory = dataclasses.get_factory(fields, entity)
        return fields, factory
    elif pydantic.is_pydantic(entity):
        fields = pydantic.get_fields(entity)
        factory = pydantic.get_factory(fields, entity)
        return fields, factory
    else:
        raise Exception
