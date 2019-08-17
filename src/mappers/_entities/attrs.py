import inspect
from typing import Any, cast

from .._types import EntityDef, EntityFactory, Fields


try:
    import attr

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def is_attrs(entity):
    # type: (Any) -> bool
    if IS_AVAILABLE:
        return inspect.isclass(entity) and attr.has(entity)
    else:
        return False


def get_fields(entity):
    # type: (EntityDef) -> Fields
    return dict(
        (attribute.name, attribute.type) for attribute in entity.__attrs_attrs__
    )


def get_factory(fields, entity):
    # type: (Fields, EntityDef) -> EntityFactory
    return cast(EntityFactory, entity)
