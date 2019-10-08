"""
mappers
-------

This module implements Declarative mappers from ORM models to domain entities.

:copyright: (c) 2019 dry-python team.
:license: BSD, see LICENSE for more details.
"""
from _mappers.mapper import Evaluated
from _mappers.mapper import mapper_factory as Mapper


__all__ = ["Evaluated", "Mapper"]
