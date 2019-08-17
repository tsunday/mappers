from typing import List

from django_project import models


def get(name, mapper, *args):
    return globals()["get_" + name](mapper, *args)


def get_load_users(mapper, user):
    @mapper.reader
    def load_users() -> List[user]:
        return models.UserModel.objects.all()

    return load_users
