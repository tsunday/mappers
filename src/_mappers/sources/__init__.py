# -*- coding: utf-8 -*-
from _mappers.exceptions import MapperError
from _mappers.sources import django


def _data_source_factory(data_source):
    if django._is_django_model(data_source):
        fields = django._get_fields(data_source)
        return fields, django._factory
    else:
        raise MapperError
