import logging
from datetime import datetime, timedelta
from random import randint

import pymysql


class Database:
    @property
    def connection(self):
        return pymysql.connect(host='dreampowerbot.ru',
                               user='u1382171',
                               password='ghob!TURK_psog6ror',
                               database='u1382171_nudes_robot')

    def execute(self, sql: str, parameters: tuple = tuple(), fetchone=False,
                fetchall=False, commit=False):

        connection = self.connection
        cursor = connection.cursor()

        cursor.execute(sql, parameters)

        data = None
        if commit:
            connection.commit()
            data = cursor.lastrowid
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()

        return data

    @staticmethod
    def format_args(sql: str, parameters: dict):
        sql += ' AND '.join([
            f"`{item}` = %s" for item in parameters
        ])
        return sql, tuple(parameters.values())

    @staticmethod
    def log(statement):
        logging.debug(statement)

    # Users

    def add_user(self, id: int):
        sql = f'INSERT INTO Users(id) VALUES({id})'
        self.execute(sql, commit=True)
        return self.get_user(id)

    def get_user(self, id: int):
        sql = f'SELECT * FROM Users WHERE `id` = {id}'
        data = self.execute(sql, fetchone=True)
        if data:
            from utils.db_api.classes.user import User
            return User(*data)

    # Links

    def get_link(self, link: str):
        sql = f'SELECT * FROM Links WHERE link = "{link}"'
        data = self.execute(sql, fetchone=True)
        if data:
            from utils.db_api.classes.link import Link
            return Link(*data)
        else:
            sql = f'INSERT INTO Links(link, hash) VALUES("{link}", "{randint(1000000000000, 10000000000000 - 1)}")'
            self.execute(sql, commit=True)
            return self.get_link(link)

