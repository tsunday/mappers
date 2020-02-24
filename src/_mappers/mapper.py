# -*- coding: utf-8 -*-
import operator
from typing import List
from typing import Optional

from _mappers.exceptions import MapperError


class Evaluated(object):
    """Mark data source field as evaluated at reading time."""

    def __init__(self, name=None):
        self.name = name


class _LazyMapper(object):
    def __init__(self, config):
        self.config = config


class _Mapper(object):
    def __init__(self, entity, data_source, config, iterable):
        self.entity = entity
        self.data_source = data_source
        self.config = config
        self.iterable = iterable

    @property
    def reader(self):
        return _ReaderGetter(self.iterable, self.entity)


class _ReaderGetter(object):
    def __init__(self, iterable, entity):
        self.iterable = iterable
        self.entity = entity
        self.ret = None

    def __call__(self, f):
        if self.ret is None:
            self.ret = getattr(f, "__annotations__", {}).get("return")
        return _Reader(f, self.iterable, self.entity, self.ret)

    def of(self, ret):
        self.ret = ret
        return self


class _Reader(object):
    def __init__(self, f, iterable, entity, ret):
        self.f = f
        self.iterable = iterable
        self.converter = _get_converter(ret, entity)

    def __call__(self, *args, **kwargs):
        return self.converter(self.raw(*args, **kwargs))

    def raw(self, *args, **kwargs):
        return self.iterable(self.f(*args, **kwargs))


def _get_converter(ret, entity):
    if ret is entity:
        return operator.methodcaller("get")
    elif ret == List[entity]:
        return list
    elif ret == Optional[entity]:
        return operator.methodcaller("first")
    else:
        raise MapperError
