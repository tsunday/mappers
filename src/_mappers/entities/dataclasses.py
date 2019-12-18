from __future__ import absolute_import

import inspect


try:
    import dataclasses

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def _is_dataclass(entity):
    if IS_AVAILABLE:
        return inspect.isclass(entity) and dataclasses.is_dataclass(entity)
    else:
        return False


def _get_fields(entity):
    return [(field.name, field.type) for field in dataclasses.fields(entity)]


def _get_factory(fields, entity):
    return entity
