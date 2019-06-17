from datetime import datetime
from typing import NewType

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
