#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright (c) 2015 DY.Feng <yyfeng88625@gmail.com>
# All rights reserved


"""此包来源自https://github.com/dcramer/django-uuidfield ，因其依赖psycopg2，而psycopg2的uuid令人不甚满意，故hack之。
我也fork了一份此修改版的在github https://github.com/DYFeng/django-uuidfield。
"""

__author__ = [
    'DY.Feng <yyfeng88625@gmail.com>',
]

import uuid
class StringUUID(uuid.UUID):
    def __init__(self, *args, **kwargs):
        # get around UUID's immutable setter
        object.__setattr__(self, 'hyphenate', kwargs.pop('hyphenate', False))

        super(StringUUID, self).__init__(*args, **kwargs)

    def __str__(self):
        if self.hyphenate:
            return super(StringUUID, self).__str__()

        return self.hex

    def __len__(self):
        return len(self.__str__())

    def to_JSON(self):
        pass

# 先把psycopg2 hack掉
import psycopg2.extras
from psycopg2 import extensions as _ext
from psycopg2.extras import UUID_adapter


def _register_uuid(oids=None, conn_or_curs=None):
    """Create the UUID type and an uuid.UUID adapter.

    :param oids: oid for the PostgreSQL :sql:`uuid` type, or 2-items sequence
        with oids of the type and the array. If not specified, use PostgreSQL
        standard oids.
    :param conn_or_curs: where to register the typecaster. If not specified,
        register it globally.
    """

    import uuid

    if not oids:
        oid1 = 2950
        oid2 = 2951
    elif isinstance(oids, (list, tuple)):
        oid1, oid2 = oids
    else:
        oid1 = oids
        oid2 = 2951

    _ext.UUID = _ext.new_type((oid1, ), "UUID",
                              lambda data, cursor: data and StringUUID(data) or None)
    _ext.UUIDARRAY = _ext.new_array_type((oid2,), "UUID[]", _ext.UUID)

    _ext.register_type(_ext.UUID, conn_or_curs)
    _ext.register_type(_ext.UUIDARRAY, conn_or_curs)
    _ext.register_adapter(StringUUID, UUID_adapter)

    return _ext.UUID


setattr(psycopg2.extras, 'register_uuid', _register_uuid)

from .fields import UUIDField