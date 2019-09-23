import inspect
from typing import Any, cast

from _mappers.types import EntityDef, EntityFactory, Fields


try:
    import dataclasses

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def is_dataclass(entity):
    # type: (Any) -> bool
    if IS_AVAILABLE:
        return inspect.isclass(entity) and dataclasses.is_dataclass(entity)
    else:
        return False


def get_fields(entity):
    # type: (EntityDef) -> Fields
    return dict((field.name, field.type) for field in dataclasses.fields(entity))


def get_factory(fields, entity):
    # type: (Fields, EntityDef) -> EntityFactory
    return cast(EntityFactory, entity)
