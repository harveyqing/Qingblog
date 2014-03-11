# -*- coding: utf-8 -*-
r"""
    _base
    ~~~~~

    Base query class of SQLAlchemy objects and
    a session mixin of SQLAlchemy objects.

    :copyright: (c) 2013 by Harvey Wang.
"""

import datetime
from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery

__all__ = ['db', 'QingQuery', 'SessionMixin']


class QingQuery(BaseQuery):

    def filter_in(self, model, values):
        values = set(values)
        if len(values) == 0:
            return {}
        if len(values) == 1:
            ident = values.pop()
            rv = self.get(ident)
            if not rv:
                return {}
            return {ident: rv}

        items = self.filter(model.in_(values))
        dic = {}
        for item in items:
            dic[getattr(item, model.key)] = item
        return dic

    def as_list(self, *columns):
        columns = map(db.defer, columns)
        return self.options(map(db.defer, columns))


class SessionMixin(object):

    def to_dict(self, *columns):
        dic = {}
        for col in columns:
            value = getattr(self, col)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
                dic[col] = value
        return dic

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


# class nullpool_SQLAlchemy(SQLAlchemy):
# 
#     def apply_driver_hacks(self, app, info, options):
#         super(nullpool_SQLAlchemy, self).apply_driver_hacks(app, info, options)
#         from sqlalchemy.pool import NullPool
#         options['poolclass'] = NullPool
#         del options['pool_size']


# db = nullpool_SQLAlchemy()
db = SQLAlchemy()
db.Model.query_class = QingQuery
