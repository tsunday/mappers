import inspect
from typing import Any

from _mappers.types import EntityDef, EntityFactory, Fields


try:
    import pydantic

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def is_pydantic(entity):
    # type: (Any) -> bool
    if IS_AVAILABLE:
        return inspect.isclass(entity) and issubclass(entity, pydantic.main.BaseModel)
    else:
        return False


def get_fields(entity):
    # type: (EntityDef) -> Fields
    return dict((key, field.type_) for key, field in entity.__fields__.items())


def get_factory(fields, entity):
    # type: (Fields, EntityDef) -> EntityFactory
    return lambda *row: entity(**{k: v for k, v in zip(fields, row)})
