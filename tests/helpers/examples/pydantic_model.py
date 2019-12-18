from datetime import datetime
from typing import NewType
from typing import Optional

from pydantic import BaseModel


UserId = NewType("UserId", int)


class User(BaseModel):
    primary_key: UserId
    created: datetime
    modified: datetime
    name: str
    about: str
    avatar: str


GroupId = NewType("GroupId", int)


class Group(BaseModel):
    primary_key: GroupId
    name: str


class OptionalGroup(BaseModel):
    primary_key: GroupId
    name: Optional[str]


class UserGroup(BaseModel):
    primary_key: GroupId
    name: User


ChatId = NewType("ChatId", int)


class Chat(BaseModel):
    primary_key: ChatId
    name: str
    is_hidden: bool


MessageId = NewType("MessageId", int)


class Message(BaseModel):
    primary_key: MessageId
    user: User
    text: str

    def written_by(self, user: User) -> bool:
        return self.user.primary_key == user.primary_key


class FlatMessage(BaseModel):
    primary_key: MessageId
    user_id: UserId
    text: str


class NamedMessage(BaseModel):
    primary_key: MessageId
    username: str
    text: str


class TotalMessage(BaseModel):
    primary_key: MessageId
    text: str
    total: int


DeliveryId = NewType("DeliveryId", int)


class Delivery(BaseModel):
    primary_key: DeliveryId
    message: Message
    service: str
