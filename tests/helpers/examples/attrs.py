from datetime import datetime
from typing import NewType
from typing import Optional

from attr import attrib
from attr import attrs


UserId = NewType("UserId", int)


@attrs
class User(object):
    primary_key = attrib(type=UserId)
    created = attrib(type=datetime)
    modified = attrib(type=datetime)
    name = attrib(type=str)
    about = attrib(type=str)
    avatar = attrib(type=str)


GroupId = NewType("GroupId", int)


@attrs
class Group(object):
    primary_key = attrib(type=GroupId)
    name = attrib(type=str)


@attrs
class OptionalGroup(object):
    primary_key = attrib(type=GroupId)
    name = attrib(type=Optional[str])


@attrs
class UserGroup(object):
    primary_key = attrib(type=GroupId)
    name = attrib(type=User)


ChatId = NewType("ChatId", int)


@attrs
class Chat(object):
    primary_key = attrib(type=ChatId)
    name = attrib(type=str)
    is_hidden = attrib(type=bool)


MessageId = NewType("MessageId", int)


@attrs
class Message(object):
    primary_key = attrib(type=MessageId)
    user = attrib(type=User)
    text = attrib(type=str)

    def written_by(self, user):
        return self.user.primary_key == user.primary_key


@attrs
class FlatMessage(object):
    primary_key = attrib(type=MessageId)
    user_id = attrib(type=UserId)
    text = attrib(type=str)


@attrs
class NamedMessage(object):
    primary_key = attrib(type=MessageId)
    username = attrib(type=str)
    text = attrib(type=str)


@attrs
class TotalMessage(object):
    primary_key = attrib(type=MessageId)
    text = attrib(type=str)
    total = attrib(type=int)


DeliveryId = NewType("DeliveryId", int)


@attrs
class Delivery(object):
    primary_key = attrib(type=DeliveryId)
    message = attrib(type=Message)
    service = attrib(type=str)
