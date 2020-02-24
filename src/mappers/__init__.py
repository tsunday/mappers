# -*- coding: utf-8 -*-
"""Declarative mappers from ORM models to domain entities.

:copyright: (c) 2019-2020 dry-python team.
:license: BSD, see LICENSE for more details.
"""
from _mappers.factory import mapper_factory as Mapper
from _mappers.mapper import Evaluated


__all__ = ["Evaluated", "Mapper"]
