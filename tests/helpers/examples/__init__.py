import pytest


# Fixtures.


def entities():
    try:
        import examples.dataclasses

        yield examples.dataclasses
    except (SyntaxError, ImportError):
        pass

    try:
        import examples.attrs_annotated

        yield examples.attrs_annotated
    except (SyntaxError):
        pass

    import examples.attrs

    yield examples.attrs


@pytest.fixture(params=entities())
def e():
    pass
