[![logo](https://raw.githubusercontent.com/dry-python/brand/master/logo/mappers.png)](https://github.com/dry-python/mappers)

[![azure-pipeline](https://dev.azure.com/dry-python/mappers/_apis/build/status/dry-python.mappers?branchName=master)](https://dev.azure.com/dry-python/mappers/_build/latest?definitionId=1&branchName=master)
[![codecov](https://codecov.io/gh/dry-python/mappers/branch/master/graph/badge.svg)](https://codecov.io/gh/dry-python/mappers)

---

# Declarative mappers to domain entities

## One to one mapping

### Define an entity with dataclass

```pycon

>>> from dataclasses import dataclass
>>> from datetime import datetime
>>> from typing import NewType

>>> UserId = NewType("UserId", int)

>>> @dataclass
... class User:
...     primary_key: UserId
...     created: datetime
...     modified: datetime
...     name: str
...     about: str
...     avatar: str

```

### Define data source with django model

```pycon

>>> from django.db import models

>>> class UserModel(models.Model):
...     created = models.DateTimeField(auto_now_add=True)
...     modified = models.DateTimeField(auto_now=True)
...     name = models.CharField(max_length=255)
...     about = models.TextField()
...     avatar = models.FileField()
...
...     class Meta:
...         app_label = "app"

```

### Define a reader mapper

```pycon

>>> from typing import List
>>> from mappers import Mapper

>>> from django_project.models import UserModel

>>> mapper = Mapper(User, UserModel, {"primary_key": "id"})

>>> @mapper.reader
... def load_users() -> List[User]:
...     """Load all users from the database."""
...     return UserModel.objects.all()

```

### Read list of domain entities directly from data source

```pycon

>>> load_users()  # doctest: +ELLIPSIS
[User(primary_key=..., created=datetime.datetime(...), modified=datetime.datetime(...), name='', about='', avatar=''), ...]

```

## Mapping evaluated field

### Define an entity with dataclass

```pycon

>>> from dataclasses import dataclass
>>> from typing import NewType

>>> ChatId = NewType("ChatId", int)

>>> @dataclass
... class Chat:
...     primary_key: ChatId
...     name: str
...     is_hidden: bool

```

### Define data source with django model

```pycon

>>> from django.db import models

>>> class ChatModel(models.Model):
...     name = models.CharField(max_length=255)
...     subscribers = models.ManyToManyField(
...         "UserModel",
...         related_name="chats",
...         through="ChatSubscriptionModel",
...     )
...
...     class Meta:
...         app_label = "app"

>>> class ChatSubscriptionModel(models.Model):
...     user = models.ForeignKey(
...         "UserModel",
...         related_name="chat_subscriptions",
...         on_delete=models.CASCADE,
...     )
...     chat = models.ForeignKey(
...         "ChatModel",
...         related_name="chat_subscriptions",
...         on_delete=models.CASCADE,
...     )
...
...     class Meta:
...         app_label = "app"

```

### Define a reader mapper

```pycon

>>> from django.db import models
>>> from mappers import Mapper, Evaluated

>>> from django_project.models import ChatModel, ChatSubscriptionModel

>>> mapper = Mapper(Chat, ChatModel, {
...     "primary_key": "id",
...     "is_hidden": Evaluated(),
... })

>>> @mapper.reader
... def load_chats(user: User) -> List[Chat]:
...     """Load all chats from the point of view of the logged-in user."""
...     subscription = ChatSubscriptionModel.objects.filter(
...         user=user.primary_key,
...         chat=models.OuterRef("pk")
...     )
...     chats = ChatModel.objects.annotate(
...         is_hidden=~models.Exists(subscription),
...     )
...     return chats

```

### Read list of domain entities directly from data source

```pycon

>>> load_chats(load_users()[0])  # doctest: +ELLIPSIS
[Chat(primary_key=..., name='', is_hidden=True), ...]

```

## Mapping with nested objects

### Define an entity with an nested entity

```pycon

>>> from dataclasses import dataclass
>>> from typing import NewType

>>> MessageId = NewType("MessageId", int)

>>> @dataclass
... class Message:
...     primary_key: MessageId
...     user: User
...     text: str
...
...     def written_by(self, user: User) -> bool:
...         return self.user.primary_key == user.primary_key

```

### Define data source with django model

```pycon

>>> from django.db import models

>>> class MessageModel(models.Model):
...     user = models.ForeignKey(
...         "UserModel",
...         related_name="messages",
...         on_delete=models.CASCADE,
...     )
...     text = models.TextField()
...
...     class Meta:
...         app_label = "app"

```

### Define a reader mapper

```pycon

>>> from mappers import Mapper

>>> from django_project.models import MessageModel

>>> mapper = Mapper(Message, MessageModel, {
...     "primary_key": "id",
...     "user": Mapper({
...         "primary_key": "id",
...     }),
... })

>>> @mapper.reader
... def load_messages() -> List[Message]:
...     """Load list of all messages."""
...     return MessageModel.objects.all()

```

### Read list of domain entities directly from data source

```pycon

>>> messages = load_messages()

>>> messages  # doctest: +ELLIPSIS
[Message(primary_key=..., user=User(primary_key=...), text=''), ...]

>>> messages[0].written_by(load_users()[0])
True

>>> messages[1].written_by(load_users()[0])
False

```
