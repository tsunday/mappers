from __future__ import absolute_import

import inspect

from _mappers.compat import _is_optional


try:
    import pydantic

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def _is_pydantic(entity):
    if IS_AVAILABLE:
        return inspect.isclass(entity) and issubclass(entity, pydantic.main.BaseModel)
    else:
        return False


def _get_fields(entity):
    return [
        (
            key,
            {
                "is_optional": _is_optional(field.type_),
                "is_entity": _is_pydantic(field.type_),
                "type": field.type_,
            },
        )
        for key, field in entity.__fields__.items()
    ]


def _get_factory(fields, entity):
    return lambda *row: entity(**{k: v for (k, t), v in zip(fields, row)})
