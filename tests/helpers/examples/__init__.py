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

        # The pydantic model returns str type for Optional[str] field
        # for some reason.  Probably a bug in the pydantic library.
        yield pytest.param(examples.pydantic_model, marks=pytest.mark.xfail)
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
