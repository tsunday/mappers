from __future__ import absolute_import

import inspect


try:
    import attr

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def _is_attrs(entity):
    if IS_AVAILABLE:
        return inspect.isclass(entity) and attr.has(entity)
    else:
        return False


def _get_fields(entity):
    return [(attribute.name, attribute.type) for attribute in entity.__attrs_attrs__]


def _get_factory(fields, entity):
    return entity
