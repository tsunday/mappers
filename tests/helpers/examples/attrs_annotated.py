# -*- coding: utf-8 -*-
from datetime import datetime
from typing import NewType
from typing import Optional

from attr import attrs


UserId = NewType("UserId", int)


@attrs(auto_attribs=True)
class User:
    """User domain model."""

    primary_key: UserId
    created: datetime
    modified: datetime
    name: str
    about: str
    avatar: str


GroupId = NewType("GroupId", int)


@attrs(auto_attribs=True)
class Group:
    """Group domain model."""

    primary_key: GroupId
    name: str


@attrs(auto_attribs=True)
class OptionalGroup:
    """Group domain model."""

    primary_key: GroupId
    name: Optional[str]


@attrs(auto_attribs=True)
class UserGroup:
    """Group domain model."""

    primary_key: GroupId
    name: User


ChatId = NewType("ChatId", int)


@attrs(auto_attribs=True)
class Chat:
    """Chat domain model."""

    primary_key: ChatId
    name: str
    is_hidden: bool


@attrs(auto_attribs=True)
class UserChat:
    """Chat domain model."""

    primary_key: ChatId
    name: str
    subscribers: User


MessageId = NewType("MessageId", int)


@attrs(auto_attribs=True)
class Message:
    """Message domain model."""

    primary_key: MessageId
    user: User
    text: str

    def written_by(self, user: User) -> bool:
        """Check if message was written by given user."""
        return self.user.primary_key == user.primary_key


@attrs(auto_attribs=True)
class FlatMessage:
    """Message domain model."""

    primary_key: MessageId
    user_id: UserId
    text: str


@attrs(auto_attribs=True)
class NamedMessage:
    """Message domain model."""

    primary_key: MessageId
    username: str
    text: str


@attrs(auto_attribs=True)
class TotalMessage:
    """Message domain model."""

    primary_key: MessageId
    text: str
    total: int


DeliveryId = NewType("DeliveryId", int)


@attrs(auto_attribs=True)
class Delivery:
    """Delivery domain model."""

    primary_key: DeliveryId
    message: Message
    service: str
