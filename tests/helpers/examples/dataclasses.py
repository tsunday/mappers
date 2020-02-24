# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from typing import NewType
from typing import Optional


UserId = NewType("UserId", int)


@dataclass
class User:
    """User domain model."""

    primary_key: UserId
    created: datetime
    modified: datetime
    name: str
    about: str
    avatar: str


GroupId = NewType("GroupId", int)


@dataclass
class Group:
    """Group domain model."""

    primary_key: GroupId
    name: str


@dataclass
class OptionalGroup:
    """Group domain model."""

    primary_key: GroupId
    name: Optional[str]


@dataclass
class UserGroup:
    """Group domain model."""

    primary_key: GroupId
    name: User


ChatId = NewType("ChatId", int)


@dataclass
class Chat:
    """Chat domain model."""

    primary_key: ChatId
    name: str
    is_hidden: bool


@dataclass
class UserChat:
    """Chat domain model."""

    primary_key: ChatId
    name: str
    subscribers: User


MessageId = NewType("MessageId", int)


@dataclass
class Message:
    """Message domain model."""

    primary_key: MessageId
    user: User
    text: str

    def written_by(self, user: User) -> bool:
        """Check if message was written by given user."""
        return self.user.primary_key == user.primary_key


@dataclass
class FlatMessage:
    """Message domain model."""

    primary_key: MessageId
    user_id: UserId
    text: str


@dataclass
class NamedMessage:
    """Message domain model."""

    primary_key: MessageId
    username: str
    text: str


@dataclass
class TotalMessage:
    """Message domain model."""

    primary_key: MessageId
    text: str
    total: int


DeliveryId = NewType("DeliveryId", int)


@dataclass
class Delivery:
    """Delivery domain model."""

    primary_key: DeliveryId
    message: Message
    service: str
