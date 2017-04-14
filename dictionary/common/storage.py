# -*-coding: utf-8-*-
# Author : Christopher Lee
# License: Apache License
# File   : store.py
# Date   : 2017-04-14 14-54
# Version: 0.0.1
# Description: description of this file.


import sqlite3

__version__ = '0.0.1'
__author__ = 'Chris'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class NullStorage(object):
    def __init__(self, database):
        self._db = database

    def execute(self, sql, args=()):
        pass

    def query(self, sql, args=()):
        pass


class SQLiteStorage(object):
    def __init__(self, database):
        self._connection = sqlite3.connect(database, check_same_thread=False)
        self._connection.row_factory = dict_factory

    def __del__(self):
        try:
            self._connection.close()
        except:
            pass

    def execute(self, sql, args=()):
        cursor = self._connection.cursor()

        try:
            cursor.execute(sql, args)
            self._connection.commit()
            return cursor.lastrowid
        except Exception as err:
            print(err)
        finally:
            cursor.close()

    def query(self, sql, args=(), first=True):
        cursor = self._connection.cursor()

        try:
            cursor.execute(sql, args)
            if first is True:
                return cursor.fetchone()
            return cursor.fetchall()
        except Exception as err:
            print(err)
        finally:
            cursor.close()
