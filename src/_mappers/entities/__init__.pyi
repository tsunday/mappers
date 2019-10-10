from typing import Any
from typing import Tuple

from _mappers.mapper import EntityFactory
from _mappers.mapper import Fields

def entity_fields_factory(entity: Any) -> Tuple[Fields, EntityFactory]: ...
