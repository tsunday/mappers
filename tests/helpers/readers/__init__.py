# -*- coding: utf-8 -*-
import pytest


# Fixtures.


def _readers():
    try:
        import readers.annotations

        yield readers.annotations
    except (SyntaxError, ImportError):
        pass

    try:
        import readers.arguments

        yield readers.arguments
    except (SyntaxError, ImportError):
        pass


@pytest.fixture(params=_readers())
def r(request):
    """Parametrized fixture with all possible reader definitions."""
    return request.param
