from app_lib.logger import *
from db.base_db import *
from db.database import *

log = logging.getLogger(__name__)


class select():
    __db = None
    __from = ''
    __where = ''
    __where_list = []
    __order = ''
    __limit = ''

    def __init__(self):
        self.__db = database.get_dbo()

    def __repr__(self):
        return f'SELECT {self.__from} {self.__where} {self.__order} {self.__limit}'

    def get_sql(self):
        if self.__from:
            select = f'SELECT {self.__from} {self.__where} {self.__order} {self.__limit}'
        else:
            select = None
        return select

    def get_params(self):
        return tuple(self.__where_list)

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
        log.info(from_)
        self.__from = from_
        return self

    # param where like 'field=?'
    def add_where(self, where, values=[], and_=True):
        # log.info(values)
        if self.__where:
            if and_:
                self.__where += ' AND '
            else:
                self.__where += ' OR '
            self.__where += where
        else:
            self.__where = f'WHERE {where}'
        self.__where_list.extend(values)
        log.debug(self.__where)

    # param where like 'field=?'
    def where(self, where, values=[], and_=True):
        if where:
            self.add_where(where, values, and_)

        return self

    def where_in(self, field, values, and_=True):
        where = f'`{field}` IN ('
        for value in values:
            where += '?,'
        where = where[:-1]
        where += ')'
        return self.where(where, values, and_)

    def get_where(self):
        return self.__where

    def get_where_params(self):
        return self.__where_list

    def order(self, field, desc=True):
        if isinstance(field, (list, tuple)):
            self.__order = 'ORDER BY '
            if not isinstance(desc, (list, tuple)):
                desc = [item for item in field]
                log.debug(f'order: {desc}')
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
        log.debug(self.__order)
        return self

    def limit(self, count, offset=0):
        count = int(count)
        offset = int(offset)
        if count < 0 or offset < 0:
            return False
        self.__limit = f'LIMIT {offset}, {count}'
        log.debug(self.get_sql())
        return self


if __name__ == '__main__':
    log.info('Start script')
    db = test_db(db_path='PassManager.db', db_prefix='pass_')
    select = select()
    params = ('source', 'user')
    select.sfrom('passwords', params)
    select.where('ID=?', [41])
    select.order('id')
    select.limit(2)
