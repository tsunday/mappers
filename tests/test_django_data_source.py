import pytest

from mappers import Mapper


pytestmark = pytest.mark.django_db

management = pytest.importorskip("django.core.management")
models = pytest.importorskip("django_project.models")


@pytest.fixture(scope="session", autouse=True)
def _loaddata(django_db_setup, django_db_blocker):
    """Populate the database with initial test data."""
    with django_db_blocker.unblock():
        management.call_command("loaddata", "examples.yaml")


# Reader.


def test_apply_result_converter(e, r):
    """
    Infer collection converter from the function result annotation.

    This code should return a list of `User` instances.
    """
    mapper = Mapper(e.User, models.UserModel, {"primary_key": "id"})

    load_users = r.get("load_users", mapper, e.User)

    user1, user2 = load_users()

    assert isinstance(user1, e.User)
    assert isinstance(user2, e.User)
