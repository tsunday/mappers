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
    except SyntaxError:
        pass

    import examples.attrs

    yield examples.attrs

    try:
        import examples.pydantic_model

        yield examples.pydantic_model
    except (SyntaxError, ImportError):
        pass

    try:
        import examples.pydantic_dataclasses

        yield examples.pydantic_dataclasses
    except (SyntaxError, ImportError):
        pass


@pytest.fixture(params=entities())
def e(request):
    return request.param
