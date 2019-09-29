import inspect


try:
    import dataclasses

    IS_AVAILABLE = True
except ImportError:
    IS_AVAILABLE = False


def is_dataclass(entity):
    if IS_AVAILABLE:
        return inspect.isclass(entity) and dataclasses.is_dataclass(entity)
    else:
        return False


def get_fields(entity):
    return dict((field.name, field.type) for field in dataclasses.fields(entity))


def get_factory(fields, entity):
    return entity
