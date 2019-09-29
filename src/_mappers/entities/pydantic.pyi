from typing import Any

from _mappers.mapper import EntityDef, EntityFactory, Fields


def is_pydantic(entity: Any) -> bool: ...


def get_fields(entity: EntityDef) -> Fields: ...


def get_factory(fields: Fields, entity: EntityDef) -> EntityFactory: ...
