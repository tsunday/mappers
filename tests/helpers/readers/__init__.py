import pytest


# Fixtures.


def readers():
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


@pytest.fixture(params=readers())
def r(request):
    return request.param
