# -*- coding: utf-8 -*-
import pytest


# Fixtures.


def _models():
    import django.core.management
    import django_project.models

    def django_models():
        django.core.management.call_command("loaddata", "examples.yaml")
        return django_project.models

    yield django_models


@pytest.fixture(params=_models())
def m(request):
    """Parametrized fixture with all possible data sources."""
    return request.param()
