import logging
import logging.config
from app_lib import log_config
from abstract_db import *


class select():
    __db = None
    __from = ''
    __where = ''
    __where_list = []
    __order = ''
    __limit = ''
    logger = None

    def __init__(self, db):
        self.__db = db
        logging.config.dictConfig(log_config.LOGGING)
        self.logger = logging.getLogger(__name__)

    def get_sql(self):
        if self.__from:
            select = f'SELECT {self.__from} {self.__where} {self.__order} {self.__limit}'
        else:
            select = None
        self.logger.debug(f'get_sql: {select}')
        return select

    def get_params(self):
        params = []
        params.extend(self.__where_list)
        params = tuple(params)
        return params

    def sfrom(self, table_name, fields):
        table_name = self.__db.get_table_name(table_name)
        from_ = ''
        if fields == '*':
            from_ = '*'
        else:
            for field in fields:
                # Проверка не является ли поле функцией напр.:COUNT(`id`)
                # т.е. преобразуем вид COUNT(id) в COUNT(`id`), а не `COUNT(id)`
                pos_1 = field.find('(')
                if pos_1 == -1:
                    from_ += f'`{field}`,'
                else:
                    pos_2 = field.find(')')
                    from_ += f'{field[:pos_1]}(`{field[pos_1+1:pos_2]}`),'
            from_ = from_[:-1]
        from_ += f' FROM `{table_name}`'
        self.logger.info(from_)
        self.__from = from_
        return self

    def add_where(self, where, values=[], and_=True):
        # self.logger.info(values)
        if self.__where:
            if and_:
                self.__where += ' AND '
            else:
                self.__where += ' OR '
            self.__where += where
        else:
            self.__where = f'WHERE {where}'
        self.__where_list.extend(values)

    def where(self, where, values=[], and_=True):
        if where:
            self.add_where(where, values, and_)
        return self

    def get_where(self):
        return self.__where

    def get_where_params(self):
        return self.__where_list

    def order(self, field, desc=True):
        if isinstance(field, (list, tuple)):
            self.__order = 'ORDER BY '
            if not isinstance(desc, (list, tuple)):
                desc = [item for item in field]
                self.logger.debug(f'order: {desc}')
            for index, item in enumerate(field):
                self.__order += f'`{item}`'
                if not desc[index]:
                    self.__order += 'DESC,'
                else:
                    self.__order += ','
            self.__order[:-1]
        else:
            self.__order = f'ORDER BY `{field}`'
            if not desc:
                self.__order += ' DESC'
        self.logger.debug(self.__order)
        return self

    def limit(self, count, offset=0):
        count = int(count)
        offset = int(offset)
        if count < 0 or offset < 0:
            return False
        self.__limit = f'LIMIT {offset}, {count}'
        self.logger.debug(self.get_sql())
        return self


if __name__ == '__main__':
    db = test_db(db_path='PassManager.db', db_prefix='pass_')
    select = select(db)
    params = ('source', 'user')
    select.sfrom('passwords', params)
    select.where('ID=?', [41])
    select.order('id')
    select.limit(2)
