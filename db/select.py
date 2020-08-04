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

    def order(self, field, ask=True):
        pass

    def limit(self, count, offset=0):
        count = int(count)
        offset = int(offset)
        if count < 0 or offset < 0:
            return False
        limit = f'LIMIT {offset}, {count}'
        return self


if __name__ == '__main__':
    db = test_db(db_path='PassManager.db', db_prefix='pass_')
    select = select(db)
    params = ('source', 'user')
    select.sfrom('passwords', params)
    select.where('ID=?', [41])
    db.get_result_set(select)
