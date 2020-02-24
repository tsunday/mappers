# -*- coding: utf-8 -*-
from __future__ import absolute_import

import inspect

from _mappers.compat import _is_optional

try:
    import attr

    IS_AVAILABLE = True
except ImportError:  # pragma: no cover
    IS_AVAILABLE = False


def _is_attrs(entity):
    if IS_AVAILABLE:
        return inspect.isclass(entity) and attr.has(entity)
    else:
        return False  # pragma: no cover


def _get_fields(entity):
    return [
        (
            attribute.name,
            {
                "is_optional": _is_optional(attribute.type),
                "is_entity": _is_attrs(attribute.type),
                "type": attribute.type,
            },
        )
        for attribute in entity.__attrs_attrs__
    ]


def _get_factory(fields, entity):
    return entity
