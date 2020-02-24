# -*- coding: utf-8 -*-
from typing import List
from typing import Optional

from django.db.models import Count

from django_project import models


def get(name, mapper, *args):
    """Define reader function."""
    return globals()["_get_" + name](mapper, *args)


def _get_load_users(mapper, user):
    @mapper.reader
    def load_users() -> List[user]:
        return models.UserModel.objects.all()

    return load_users


def _get_load_user(mapper, user, user_id):
    @mapper.reader
    def load_user(primary_key: user_id) -> user:
        return models.UserModel.objects.filter(pk=primary_key)

    return load_user


def _get_load_user_or_none(mapper, user, user_id):
    @mapper.reader
    def load_user(primary_key: user_id) -> Optional[user]:
        return models.UserModel.objects.filter(pk=primary_key)

    return load_user


def _get_load_messages(mapper, message):
    @mapper.reader
    def load_messages() -> List[message]:
        return models.MessageModel.objects.all()

    return load_messages


def _get_load_total_messages(mapper, message, field_name):
    @mapper.reader
    def load_messages() -> List[message]:
        q = {field_name: Count("user_id")}
        return models.MessageModel.objects.annotate(**q)

    return load_messages


def _get_load_deliveries(mapper, delivery):
    @mapper.reader
    def load_deliveries() -> List[delivery]:
        return models.MessageDeliveryModel.objects.all()

    return load_deliveries


def _get_load_groups(mapper, group):
    @mapper.reader
    def load_groups() -> List[group]:
        return models.GroupModel.objects.all()

    return load_groups


def _get_invalid_converter(mapper, value):
    @mapper.reader
    def invalid() -> value:
        pass  # pragma: no cover
