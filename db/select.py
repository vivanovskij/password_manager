import logging
import logging.config
from app_lib import log_config
from abstract_db import *


class select():
    __db = None
    __from = None
    __where = None
    __order = None
    __limit = None
    logger = None

    def __init__(self, db):
        self.__db = db
        logging.config.dictConfig(log_config.LOGGING)
        self.logger = logging.getLogger(__name__)

    def add_where(self, where, and_=True):
        if self.__where:
            if and_:
                self.__where += ' AND '
            else:
                self.__where += ' OR '
        else:
            self.__where = f'WHERE {where}'

    def from_(self, table_name, fields):
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


if __name__ == '__main__':
    db = test_db(db_path='test.db', db_prefix='test_')
    test = select(db)
    params = ('COUNT(user)', 'name', 'password')
    test.from_('table', params)
