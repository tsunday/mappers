from datetime import datetime
from typing import NewType
from typing import Optional

from pydantic.dataclasses import dataclass


UserId = NewType("UserId", int)


@dataclass
class User:
    primary_key: UserId
    created: datetime
    modified: datetime
    name: str
    about: str
    avatar: str


GroupId = NewType("GroupId", int)


@dataclass
class Group:
    primary_key: GroupId
    name: str


@dataclass
class OptionalGroup:
    primary_key: GroupId
    name: Optional[str]


@dataclass
class UserGroup:
    primary_key: GroupId
    name: User


ChatId = NewType("ChatId", int)


@dataclass
class Chat:
    primary_key: ChatId
    name: str
    is_hidden: bool


MessageId = NewType("MessageId", int)


@dataclass
class Message:
    primary_key: MessageId
    user: User
    text: str

    def written_by(self, user: User) -> bool:
        return self.user.primary_key == user.primary_key


@dataclass
class FlatMessage:
    primary_key: MessageId
    user_id: UserId
    text: str


@dataclass
class NamedMessage:
    primary_key: MessageId
    username: str
    text: str


@dataclass
class TotalMessage:
    primary_key: MessageId
    text: str
    total: int


DeliveryId = NewType("DeliveryId", int)


@dataclass
class Delivery:
    primary_key: DeliveryId
    message: Message
    service: str
