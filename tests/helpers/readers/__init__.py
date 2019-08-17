import pytest


# Fixtures.


def readers():
    try:
        import readers.annotations

        yield readers.annotations
    except SyntaxError:
        pass

    import readers.arguments

    yield readers.arguments


@pytest.fixture(params=readers())
def r(request):
    return request.param
