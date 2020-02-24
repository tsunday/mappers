# -*- coding: utf-8 -*-
import pytest


# Fixtures.


def _entities():
    try:
        import examples.dataclasses

        yield examples.dataclasses
    except (SyntaxError, ImportError):
        pass

    try:
        import examples.attrs_annotated

        yield examples.attrs_annotated
    except SyntaxError:
        pass

    import examples.attrs

    yield examples.attrs

    try:
        import examples.pydantic_model

        # The pydantic model returns str type for Optional[str] field
        # for some reason.  Probably a bug in the pydantic library.
        yield examples.pydantic_model
    except (SyntaxError, ImportError):
        pass

    try:
        import examples.pydantic_dataclasses

        yield examples.pydantic_dataclasses
    except (SyntaxError, ImportError):
        pass


@pytest.fixture(params=_entities())
def e(request):
    """Parametrized fixture with all possible entity definitions."""
    return request.param
