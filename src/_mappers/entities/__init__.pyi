from typing import Any
from typing import List
from typing import Tuple
from typing import Type

from typing_extensions import Protocol
from typing_extensions import TypedDict

_FieldName = str

class _FieldDef(TypedDict):
    is_optional: bool
    is_entity: bool
    type: Type[Any]

_EntityField = Tuple[_FieldName, _FieldDef]

_EntityFields = List[_EntityField]

_Entity = Any

_EntityClass = Type[_Entity]

class _EntityFactory(Protocol):
    def __call__(self, *row: Any) -> _Entity: ...

def _entity_factory(entity: Any) -> Tuple[_EntityFields, _EntityFactory]: ...
