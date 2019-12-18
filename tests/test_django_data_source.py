"""Tests related to the Django models data source."""
from logging import Logger

import pytest

from mappers import Evaluated
from mappers import Mapper
from mappers.exceptions import MapperError


pytestmark = pytest.mark.django_db

management = pytest.importorskip("django.core.management")
QuerySet = pytest.importorskip("django.db.models").QuerySet
models = pytest.importorskip("django_project.models")


@pytest.fixture(scope="session", autouse=True)
def _loaddata(django_db_setup, django_db_blocker):
    """Populate the database with initial test data."""
    with django_db_blocker.unblock():
        management.call_command("loaddata", "examples.yaml")


# Converters.


def test_result_raw_method(e, r):
    """
    Provide a way to access underling iterable object.

    This code should return a queryset of `User` instances.
    """
    mapper = Mapper(e.User, models.UserModel, {"primary_key": "id"})

    load_users = r.get("load_users", mapper, e.User)

    result = load_users.raw()

    assert isinstance(result, QuerySet)

    result = iter(result)
    user1 = next(result)
    user2 = next(result)

    assert isinstance(user1, e.User)
    assert isinstance(user2, e.User)

    with pytest.raises(StopIteration):
        next(result)


def test_result_list_converter(e, r):
    """
    Infer collection converter from the function result annotation.

    This code should return a list of `User` instances.
    """
    mapper = Mapper(e.User, models.UserModel, {"primary_key": "id"})

    load_users = r.get("load_users", mapper, e.User)

    result = load_users()

    assert isinstance(result, list)

    user1, user2 = result

    assert isinstance(user1, e.User)
    assert isinstance(user2, e.User)


def test_result_object_converter(e, r):
    """
    Return a single object.

    If instead of converter annotation will be an entity class, we
    should return a single object.  Not a collection.
    """
    mapper = Mapper(e.User, models.UserModel, {"primary_key": "id"})

    load_user = r.get("load_user", mapper, e.User, e.UserId)

    user1 = load_user(1)

    assert isinstance(user1, e.User)

    with pytest.raises(models.UserModel.DoesNotExist):
        load_user(3)


def test_result_optional_converter(e, r):
    """
    Return a single object or None.

    If annotation of the reader will be an optional entity class, we
    should not raise DoesNotExist error.  Instead of this we will
    return None.
    """
    mapper = Mapper(e.User, models.UserModel, {"primary_key": "id"})

    load_user = r.get("load_user_or_none", mapper, e.User, e.UserId)

    user1 = load_user(1)

    assert isinstance(user1, e.User)

    user3 = load_user(3)

    assert user3 is None


@pytest.mark.parametrize("value", [None, False, Logger])
def test_result_unknown_converter(e, r, value):
    """
    Raise error in unclear situation.

    If annotation of the reader will be something unknown, we should
    raise MapperError.
    """
    mapper = Mapper(e.User, models.UserModel, {"primary_key": "id"})

    expected = ""

    with pytest.raises(MapperError) as exc_info:
        r.get("invalid_converter", mapper, value)

    message = str(exc_info.value)
    assert message == expected


# Nested mappers.


def test_nested_mapper(e, r):
    """
    Set mapper as a field of another mapper.

    Entities could contains nested entities.  Mappers of nested
    entities should be expressed as nested mappers in the config.

    This code should return a list of `Message` instances.  Each
    `Message` instance should have `User` instance as its attribute.
    """
    mapper = Mapper(
        e.Message,
        models.MessageModel,
        {"primary_key": "id", "user": Mapper({"primary_key": "id"})},
    )

    load_messages = r.get("load_messages", mapper, e.Message)

    result = load_messages()

    assert isinstance(result, list)

    message1, message2 = result

    assert isinstance(message1, e.Message)
    assert isinstance(message2, e.Message)
    assert isinstance(message1.user, e.User)
    assert isinstance(message2.user, e.User)


def test_deep_nested_mapper(e, r):
    """
    Set mapper as a field of another field.

    Nested entities could contain nested entities as well.  Mappers of
    nested entities should contain nested mappers as well.

    This code should return a list of `Delivery` instances.  Each
    `Delivery` instance should have `Message` instance as its
    attribute.  Each `Message` instance should have `User` as its
    attribute.
    """
    mapper = Mapper(
        e.Delivery,
        models.MessageDeliveryModel,
        {
            "primary_key": "id",
            "message": Mapper(
                {"primary_key": "id", "user": Mapper({"primary_key": "id"})}
            ),
        },
    )

    load_deliveries = r.get("load_deliveries", mapper, e.Delivery)

    result = load_deliveries()

    assert isinstance(result, list)

    delivery1, delivery2 = result

    assert isinstance(delivery1, e.Delivery)
    assert isinstance(delivery2, e.Delivery)
    assert isinstance(delivery1.message, e.Message)
    assert isinstance(delivery2.message, e.Message)
    assert isinstance(delivery1.message.user, e.User)
    assert isinstance(delivery2.message.user, e.User)


# Related fields.


def test_related_field(e, r):
    """
    Set field of the related data source to the entity field.

    Mapper could point any field of the entity to any field of any
    related model of the mapped data source.
    """
    mapper = Mapper(
        e.NamedMessage,
        models.MessageModel,
        {"primary_key": "id", "username": ("user", "name")},
    )

    load_messages = r.get("load_messages", mapper, e.NamedMessage)

    result = load_messages()

    assert isinstance(result, list)

    message1, message2 = result

    assert isinstance(message1, e.NamedMessage)
    assert isinstance(message2, e.NamedMessage)
    assert message1.username == ""
    assert message2.username == ""


def test_resolve_id_field_from_foreign_key_without_config(e, r):
    """
    Use foreign key as a field.

    Original data source model could have foreign key field defined.
    The actual entity may require only id value with out whole related
    object.

    Code below should work with out config specifics of the `user`
    field.
    """
    mapper = Mapper(e.FlatMessage, models.MessageModel, {"primary_key": "id"})

    load_messages = r.get("load_messages", mapper, e.FlatMessage)

    result = load_messages()

    assert isinstance(result, list)

    message1, message2 = result

    assert isinstance(message1, e.FlatMessage)
    assert isinstance(message2, e.FlatMessage)
    assert message1.user_id == 1
    assert message2.user_id == 2


# Evaluated fields.


def test_evaluated_field(e, r):
    """
    Evaluate fields which are not declared in the data source.

    Evaluated marker should be interpreted as a reason to ignore
    absence of the field directly on the data source model.  Field
    with exactly this name will appears on the collection.
    """
    mapper = Mapper(
        e.TotalMessage, models.MessageModel, {"primary_key": "id", "total": Evaluated()}
    )

    load_messages = r.get("load_total_messages", mapper, e.TotalMessage, "total")

    result = load_messages()

    assert isinstance(result, list)

    message1, message2 = result

    assert isinstance(message1, e.TotalMessage)
    assert isinstance(message2, e.TotalMessage)
    assert message1.total == 1
    assert message2.total == 1


def test_named_evaluated_field(e, r):
    """
    Use custom name in the data source for the evaluation result.

    Evaluated marker could be pointed to the field with a different
    name than the target attribute.
    """
    mapper = Mapper(
        e.TotalMessage,
        models.MessageModel,
        {"primary_key": "id", "total": Evaluated("total_number")},
    )

    load_messages = r.get("load_total_messages", mapper, e.TotalMessage, "total_number")

    result = load_messages()

    assert isinstance(result, list)

    message1, message2 = result

    assert isinstance(message1, e.TotalMessage)
    assert isinstance(message2, e.TotalMessage)
    assert message1.total == 1
    assert message2.total == 1


# Validation.


def test_data_source_field_missing(e):
    """
    Detect if data source field set is not complete.

    Raise exception if data source missed some fields required by
    entity.  And there is no configuration related to the field.
    """
    expected = ("Can not find 'primary_key' field in the %s model") % (
        models.UserModel,
    )

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.User, models.UserModel)

    message = str(exc_info.value)
    assert message == expected


def test_nullable_field_validation(e):
    """
    Detect if data source field breaks the contract.

    Data source cannot have nullable field if corresponding entity
    attribute is not annotated with Optional type.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.Group, models.GroupModel, {"primary_key": "id"})

    message = str(exc_info.value)
    assert message == expected


def test_nullable_field_optional_attribute(e, r):
    """
    Detect if data source field follows the contract.

    Data source can have nullable field if corresponding entity
    attribute annotated with Optional type.
    """
    mapper = Mapper(e.OptionalGroup, models.GroupModel, {"primary_key": "id"})

    load_groups = r.get("load_groups", mapper, e.OptionalGroup)

    result = load_groups()

    assert isinstance(result, list)

    group1, group2 = result

    assert isinstance(group1, e.OptionalGroup)
    assert isinstance(group2, e.OptionalGroup)
    assert group1.name is None
    assert group2.name == ""


def test_nested_entities_field_validation(e):
    """
    Detect if data source relations breaks the contract.

    Entity cannot have nested entity field whily data source field is
    not a relation field.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.UserGroup, models.GroupModel, {"primary_key": "id"})

    message = str(exc_info.value)
    assert message == expected


@pytest.mark.parametrize("value", ["text", Evaluated()])
def test_nested_entities_config_validation(e, value):
    """
    Detect invalid config definition.

    Mapper cannot have definition of the nested entity field which is
    not a Mapper.
    """
    expected = ""

    with pytest.raises(MapperError) as exc_info:
        Mapper(e.Message, models.MessageModel, {"primary_key": "id", "user": value})

    message = str(exc_info.value)
    assert message == expected
