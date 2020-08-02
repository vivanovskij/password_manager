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

    # query - sql query
    # params - must be a tuple
    # return dictionary where key = query(str), value = params(tuple)

    def create_query_dict(self, query, params):
        if params:
            args = []
            for item in params:
                if not item:
                    item = 'NULL'
                args.append(item)
            args = tuple(args)
            query_dict = {f'{query}': args}
        return query_dict

    def query_execute(self, query_dict):
        if query_dict:
            sql = ''
            args = ()
            for item in query_dict:
                sql += f' {item}'
                args += query_dict[item]
            self.logger.info(sql)
            self.logger.info(args)
            # return self.__cursor.execute(sql, args)

    def get_table_name(self, table_name):
        return self.__prefix + table_name

    def select(self, select):
        result_set = self.result_set()

    def result_set(self, zero=True, one=True):
        result_set = self.__cursor.execute()


class test_db(abstract_db):
    pass


if __name__ == '__main__':
    logging.config.dictConfig(log_config.LOGGING)
    logger = logging.getLogger(__name__)

    db = test_db('test.db', 'test')

    qselect = 'SELECT ? ? ?'
    qfrom = 'FROM ?'
    params1 = ('one', 'two', None)
    params2 = (None,)
    query_dict1 = db.create_query_dict(qselect, params1)
    logger.info(query_dict1)
    query_dict2 = db.create_query_dict(qfrom, params2)
    logger.info(query_dict2)
    query_dict = {**query_dict1, **query_dict2}
    logger.info(query_dict)
    db.query_execute(query_dict)
