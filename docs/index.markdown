[![Mappers](https://raw.githubusercontent.com/dry-python/brand/master/logo/mappers.png)](https://github.com/dry-python/mappers)

-----

# Declarative mappers to domain entities

## One to one mapping

### Define an entity with dataclass

```python

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

```python

>>> from django.db import models

>>> class UserModel(models.Model):
...     created = models.DateTimeField(auto_now_add=True)
...     modified = models.DateTimeField(auto_now=True)
...     name = models.CharField(max_length=255)
...     about = models.TextField()
...     avatar = models.ImageField()

```

### Define the mapper

```python

>>> from typing import List
>>> from mappers import Mapper

>>> mapper = Mapper(User, UserModel)

>>> @mapper.reader
... def load_users() -> List[User]:
...     """Load all users from the database."""
...     return UserModel.objects.all()

```

### Read list of domain entities directly from data source

```python

>>> load_users()
[User(primary_key=..., created=datetime.datetime(...), modified=datetime.datetime(...), name='', about='', avatar=''), ...]

```
