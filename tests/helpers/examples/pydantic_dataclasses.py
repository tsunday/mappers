from datetime import datetime
from typing import NewType

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
