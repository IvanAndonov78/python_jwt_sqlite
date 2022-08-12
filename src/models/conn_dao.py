import sqlite3


class ConnDao:
    def __init__(self):
        # self._connection = self.conn(self)
        self._connection = self.get_connection()

    # _ for protected members,
    # __ for private members

    @property
    def conn(self):
        return sqlite3.connect('src/database/data.db')

    @conn.setter
    def conn(self):
        self._connection = sqlite3.connect('src/database/data.db')

    @classmethod
    def get_connection(cls):
        return sqlite3.connect('src/database/data.db')
