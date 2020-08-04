import os
from abc import ABC, abstractmethod
from app_lib import log_config
import logging
import logging.config
import sqlite3
import select


class abstract_db(ABC):
    __db = None
    __cursor = None
    __prefix = ''
    logger = None

    def __init__(self, db_path='', db_prefix=''):
        # Create logger
        logging.config.dictConfig(log_config.LOGGING)
        self.logger = logging.getLogger(__name__)

        # Prefix for database
        self.__prefix = db_prefix

        # Connect to database
        try:
            self.__db = sqlite3.connect(db_path)
        except sqlite3.DatabaseError as err:
            self.logger.error('Error connection to database')
        else:
            self.logger.info('block Else')
            self.__cursor = self.__db.cursor()
            # self.__cursor.execute("SET lc_time_names = 'ru_RU'")

    def __del__(self):
        self.__db.close()

    def query(self, query, params=None):
        if params:
            for item in params:
                if not item:
                    item = 'NULL'
        try:
            self.__cursor.execute(query, params)
        except sqlite3.DatabaseError as err:
            self.logger.error(err)
            return False
        else:
            self.__db.commit()
        if self.__cursor.lastrowid == 0:
            return True
        return self.__cursor.lastrowid

    def select(self, select):
        result_set = self.__cursor.execute(
            select.get_sql(), select.get_params())
        if not result_set:
            return False
        return result_set

    def select_row(self, select):
        result_set = self.select(select).fetchone()
        if not result_set:
            return False
        return result_set

    def select_col(self, select):
        result_set = self.select(select).fetchall()
        if not result_set:
            return False
        return result_set

    def select_cell(self, select):
        result_set = self.select(select).fetchone()
        if not result_set:
            return False
        return result_set[0]

    def get_table_name(self, table_name):
        return self.__prefix + table_name


class test_db(abstract_db):
    pass


if __name__ == '__main__':
    db = test_db(db_path='PassManager.db', db_prefix='pass_')
    select = select.select(db)
    # params = ('source',)
    params = '*'
    select.sfrom('passwords', params)
    select.where('Login=?', ['Килобайт'])
    print(db.select_cell(select))
