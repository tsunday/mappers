from datetime import datetime
from typing import NewType

from pydantic import BaseModel


UserId = NewType("UserId", int)


class User(BaseModel):
    primary_key: UserId
    created: datetime
    modified: datetime
    name: str
    about: str
    avatar: str


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
