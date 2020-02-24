# -*- coding: utf-8 -*-
from datetime import datetime
from typing import NewType
from typing import Optional

from pydantic import BaseModel


UserId = NewType("UserId", int)


class User(BaseModel):
    """User domain model."""

    primary_key: UserId
    created: datetime
    modified: datetime
    name: str
    about: str
    avatar: str


GroupId = NewType("GroupId", int)


class Group(BaseModel):
    """Group domain model."""

    primary_key: GroupId
    name: str


class OptionalGroup(BaseModel):
    """Group domain model."""

    primary_key: GroupId
    name: Optional[str]


class UserGroup(BaseModel):
    """Group domain model."""

    primary_key: GroupId
    name: User


ChatId = NewType("ChatId", int)


class Chat(BaseModel):
    """Chat domain model."""

    primary_key: ChatId
    name: str
    is_hidden: bool


class UserChat(BaseModel):
    """Chat domain model."""

    primary_key: ChatId
    name: str
    subscribers: User


MessageId = NewType("MessageId", int)


class Message(BaseModel):
    """Message domain model."""

    primary_key: MessageId
    user: User
    text: str

    def written_by(self, user: User) -> bool:
        """Check if message was written by given user."""
        return self.user.primary_key == user.primary_key


class FlatMessage(BaseModel):
    """Message domain model."""

    primary_key: MessageId
    user_id: UserId
    text: str


class NamedMessage(BaseModel):
    """Message domain model."""

    primary_key: MessageId
    username: str
    text: str


class TotalMessage(BaseModel):
    """Message domain model."""

    primary_key: MessageId
    text: str
    total: int


DeliveryId = NewType("DeliveryId", int)


class Delivery(BaseModel):
    """Delivery domain model."""

    primary_key: DeliveryId
    message: Message
    service: str
