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
from _mappers.sources.django import ValuesList

_Config = Dict[str, Union[str, LazyMapper, Mapper, Evaluated, Tuple[str, ...]]]

class Evaluated:
    def __init__(self, name: Optional[str] = ...) -> None: ...

class LazyMapper:
    def __init__(self, config: _Config) -> None: ...
    def build(self, entity: _EntityClass, data_source: _DataSource) -> Mapper: ...

class Mapper:
    def __init__(
        self,
        entity: _EntityClass,
        data_source: _DataSource,
        config: _Config,
        iterable: ValuesList,
    ) -> None: ...
    @property
    def reader(self) -> ReaderGetter: ...

class ReaderGetter:
    def __init__(self, iterable: ValuesList, entity: _EntityClass) -> None: ...
    def __call__(self, f: Callable) -> Reader: ...
    def of(self, ret: _SpecialForm) -> ReaderGetter: ...

class Reader:
    def __init__(
        self, f: Callable, iterable: ValuesList, entity: _EntityClass, ret: _SpecialForm
    ) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    def raw(self, *args: Any, **kwargs: Any) -> Iterable: ...

def get_converter(ret: _SpecialForm, entity: _EntityClass) -> Callable: ...
