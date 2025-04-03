"""
Модуль описывает репозиторий, работающий в базе данных SQLite
"""

import sqlite3
from typing import Any
from inspect import get_annotations

from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SQLiteRepository(AbstractRepository[T]):

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        self.obj_cls = cls

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute('SELECT name FROM sqlite_master')
            db_tables = [t[0].lower() for t in res.fetchall()]
            if self.table_name not in db_tables:
                col_names = ', '.join(self.fields.keys())
                query = f'CREATE TABLE {self.table_name} (' \
                    f'"pk" INTEGER PRIMARY KEY AUTOINCREMENT, {col_names})'
                cur.execute(query)
        con.close()

    def add(self, obj: T) -> int:
        """ Добавляет объект в базу данных """
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        param = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({param})', values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        """ Получить объект по id """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'SELECT * FROM {self.table_name} WHERE ROWID=={pk}'
            )
            res = cur.fetchall()
        con.close()
        if not res:
            obj = None
        else:
            res = res[0]
            kwargs = dict(zip(self.fields, res[1:]))
            obj = self.obj_cls(**kwargs)
            obj.pk = pk
        return obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            if where is None:
                res_s = cur.execute(f'SELECT * FROM {self.table_name}').fetchall()
            else:
                fields = " AND ".join([f"{f} LIKE ?" for f in where.keys()])
                res_s = cur.execute(
                    f'SELECT * FROM {self.table_name} ' + f'WHERE {fields}',
                    list(where.values())).fetchall()
        obj_s = []
        for res in res_s:
            kwargs = dict(zip(self.fields, res[1:]))
            obj = self.obj_cls(**kwargs)
            obj.pk = res[0]
            obj_s.append(obj)
        return obj_s

    def update(self, obj: T) -> None:
        """ Заменить объект по id """
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')

        fields = ", ".join([f"{f}=?" for f in self.fields.keys()])
        values = [getattr(obj, f) for f in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'UPDATE {self.table_name} SET {fields} WHERE ROWID=={obj.pk}', values
            )
        con.close()

    def delete(self, pk: int) -> None:
        """ Удалить объект по id """
        if pk == 0:
            raise ValueError('attempt to delete object with unknown primary key')
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'DELETE FROM {self.table_name} WHERE pk = {pk}')
            deleted_count = cur.rowcount
        con.close()
        if deleted_count == 0:
            raise KeyError