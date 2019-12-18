from datetime import datetime
from typing import NewType
from typing import Optional

from attr import attrs


UserId = NewType("UserId", int)


@attrs(auto_attribs=True)
class User:
    primary_key: UserId
    created: datetime
    modified: datetime
    name: str
    about: str
    avatar: str


GroupId = NewType("GroupId", int)


@attrs(auto_attribs=True)
class Group:
    primary_key: GroupId
    name: str


@attrs(auto_attribs=True)
class OptionalGroup:
    primary_key: GroupId
    name: Optional[str]


@attrs(auto_attribs=True)
class UserGroup:
    primary_key: GroupId
    name: User


ChatId = NewType("ChatId", int)


@attrs(auto_attribs=True)
class Chat:
    primary_key: ChatId
    name: str
    is_hidden: bool


MessageId = NewType("MessageId", int)


@attrs(auto_attribs=True)
class Message:
    primary_key: MessageId
    user: User
    text: str

    def written_by(self, user: User) -> bool:
        return self.user.primary_key == user.primary_key


@attrs(auto_attribs=True)
class FlatMessage:
    primary_key: MessageId
    user_id: UserId
    text: str


@attrs(auto_attribs=True)
class NamedMessage:
    primary_key: MessageId
    username: str
    text: str


@attrs(auto_attribs=True)
class TotalMessage:
    primary_key: MessageId
    text: str
    total: int


DeliveryId = NewType("DeliveryId", int)


@attrs(auto_attribs=True)
class Delivery:
    primary_key: DeliveryId
    message: Message
    service: str
