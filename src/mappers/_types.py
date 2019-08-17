import typing
from typing import Any, Dict, Tuple, Type

from typing_extensions import Protocol


Entity = Any
EntityDef = Type[Entity]
Field = Type[Any]
Fields = Dict[str, Field]
Row = Tuple[Any, ...]


class EntityFactory(Protocol):
    def __call__(self, *row):
        # type: (*Any) -> Entity
        pass


TypingDef = getattr(typing, "_SpecialForm", None)

if TypingDef is None:
    TypingDef = getattr(typing, "_TypingBase", None)

if TypingDef is None:
    raise RuntimeError
