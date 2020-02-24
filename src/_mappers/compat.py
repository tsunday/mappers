# -*- coding: utf-8 -*-
from inspect import isclass
from typing import Union

try:
    from typing import _GenericAlias
except ImportError:
    # We are on Python 2.7 and old typing module.
    class _GenericAlias(object):
        pass


try:
    from typing import _Union
except ImportError:
    # We are on Python 3.7 and new typing module.
    class _Union(object):
        pass


def _is_optional(t):
    return (
        isinstance(t, (_GenericAlias, _Union))
        and t.__origin__ is Union
        and len(t.__args__) == 2
        and isclass(t.__args__[-1])
        and isinstance(None, t.__args__[-1])
    )
