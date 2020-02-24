# -*- coding: utf-8 -*-
from datetime import datetime
from typing import NewType
from typing import Optional

from attr import attrib
from attr import attrs


UserId = NewType("UserId", int)


@attrs
class User(object):
    """User domain model."""

    primary_key = attrib(type=UserId)
    created = attrib(type=datetime)
    modified = attrib(type=datetime)
    name = attrib(type=str)
    about = attrib(type=str)
    avatar = attrib(type=str)


GroupId = NewType("GroupId", int)


@attrs
class Group(object):
    """Group domain model."""

    primary_key = attrib(type=GroupId)
    name = attrib(type=str)


@attrs
class OptionalGroup(object):
    """Group domain model."""

    primary_key = attrib(type=GroupId)
    name = attrib(type=Optional[str])


@attrs
class UserGroup(object):
    """Group domain model."""

    primary_key = attrib(type=GroupId)
    name = attrib(type=User)


ChatId = NewType("ChatId", int)


@attrs
class Chat(object):
    """Chat domain model."""

    primary_key = attrib(type=ChatId)
    name = attrib(type=str)
    is_hidden = attrib(type=bool)


@attrs
class UserChat(object):
    """Chat domain model."""

    primary_key = attrib(type=ChatId)
    name = attrib(type=str)
    subscribers = attrib(type=User)


MessageId = NewType("MessageId", int)


@attrs
class Message(object):
    """Message domain model."""

    primary_key = attrib(type=MessageId)
    user = attrib(type=User)
    text = attrib(type=str)

    def written_by(self, user):
        """Check if message was written by given user."""
        return self.user.primary_key == user.primary_key


@attrs
class FlatMessage(object):
    """Message domain model."""

    primary_key = attrib(type=MessageId)
    user_id = attrib(type=UserId)
    text = attrib(type=str)


@attrs
class NamedMessage(object):
    """Message domain model."""

    primary_key = attrib(type=MessageId)
    username = attrib(type=str)
    text = attrib(type=str)


@attrs
class TotalMessage(object):
    """Message domain model."""

    primary_key = attrib(type=MessageId)
    text = attrib(type=str)
    total = attrib(type=int)


DeliveryId = NewType("DeliveryId", int)


@attrs
class Delivery(object):
    """Delivery domain model."""

    primary_key = attrib(type=DeliveryId)
    message = attrib(type=Message)
    service = attrib(type=str)
