from typing import Any, Tuple

from _mappers.mapper import EntityFactory, Fields


def entity_fields_factory(entity: Any) -> Tuple[Fields, EntityFactory]: ...
