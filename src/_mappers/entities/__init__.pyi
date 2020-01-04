from typing import Any
from typing import List
from typing import Tuple
from typing import Type

from typing_extensions import Protocol

_Field = Type[Any]

_Fields = List[Tuple[str, _Field]]

_Entity = Any

_EntityClass = Type[_Entity]

class _EntityFactory(Protocol):
    def __call__(self, *row: Any) -> _Entity: ...

def _entity_factory(entity: Any) -> Tuple[_Fields, _EntityFactory]: ...
