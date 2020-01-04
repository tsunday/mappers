from typing import _SpecialForm
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import Union

from _mappers.entities import _EntityClass
from _mappers.sources import _DataSource
from _mappers.sources.django import _ValuesList

_RelatedField = Tuple[str, ...]

_ConfigValue = Union[str, _LazyMapper, Evaluated, _RelatedField]

_Config = Dict[str, _ConfigValue]

class Evaluated:
    def __init__(self, name: Optional[str] = ...) -> None: ...

class _LazyMapper:
    def __init__(self, config: _Config) -> None: ...

class _Mapper:
    def __init__(
        self,
        entity: _EntityClass,
        data_source: _DataSource,
        config: _Config,
        iterable: _ValuesList,
    ) -> None: ...
    @property
    def reader(self) -> _ReaderGetter: ...

class _ReaderGetter:
    def __init__(self, iterable: _ValuesList, entity: _EntityClass) -> None: ...
    def __call__(self, f: Callable) -> _Reader: ...
    def of(self, ret: _SpecialForm) -> _ReaderGetter: ...

class _Reader:
    def __init__(
        self,
        f: Callable,
        iterable: _ValuesList,
        entity: _EntityClass,
        ret: _SpecialForm,
    ) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    def raw(self, *args: Any, **kwargs: Any) -> Iterable: ...

def _get_converter(ret: _SpecialForm, entity: _EntityClass) -> Callable: ...
