from typing import List

from django_project import models


def get(name, mapper, *args):
    return globals()["get_" + name](mapper, *args)


def get_load_users(mapper, user):
    @mapper.reader.of(List[user])
    def load_users():
        return models.UserModel.objects.all()

    return load_users
