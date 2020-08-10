from db.database import *
from db.base_db import *
from db.select import *
from app_lib.logger import *
from abc import ABC
from datetime import datetime

log = logging.getLogger(__name__)


class base_object_db(ABC):
    __db = None
    __table_name = ''
    __format_date = ''
    __properties = {}

    def __init__(self, table_name):
        self.__db = database.get_dbo()
        self.__table_name = table_name
        self.__format_date = config.FORMAT_DATE
        cursor = self.__db.get_cursor()
        temp = cursor.execute(
            f'SELECT * FROM {self.__table_name}')
        for description in temp.description:
            self.__add_property(description[0])
        log.debug(self.__properties)

    # ability to get data like: obj.attr

    def __get__(self, name):
        if name in self.__properties:
            return self.__properties[name]['value']
        return None

    # ability to set data like: obj[attr]=value

    def __setitem__(self, name, value):
        if name in self.__properties:
            self.__properties[name]['value'] = value
            return True
        else:
            self.__properties[name] = {'value': value}
        # log.debug(self.__properties)

    def __add_property(self, field, default=None):
        self.__properties[field] = {'value': default}

    def get_all(self, count=False, offset=False):
        return self.get_all_with_order('id', True, count, offset)

    def get_all_with_order(self, order, ask=True, count=False, offset=False):
        return self.get_all_on_where(False, False, order, ask, count, offset)

    def get_all_on_where(self, where=False, values=False, order=False, ask=True, count=False, offset=False):
        sel = self.__get_base_select()
        if where:
            sel.where(where, values)
        if order:
            sel.order(order, ask)
        else:
            sel.order('id')
        if count:
            sel.limit(count, offset)
        log.debug(sel)
        return self.__db.select(sel)

    def get_all_on_field(self, field, value, order=False, ask=True, count=False, offset=False):
        log.debug(value)
        return self.get_all_on_where(f'`{field}`=?', (value,), order, ask, count, offset)

    def get_all_on_ids(self, ids):
        sel = self.__get_base_select()
        sel.where_in('id', ids)
        return self.__db.select(sel)

    def __get_base_select(self):
        sel = select()
        sel.sfrom(self.__table_name, '*')
        return sel

    def get_date(self, date=False):
        if not date:
            date = datetime.today()
        return date.strftime(self.__format_date)

    def get_count(self):
        pass

    def get_count_on_field(self):
        pass

    def get_count_on_where(self, table_name, where=False, values=False):
        pass

    def get_key(self):
        pass

    def get_relevant_for_search(self, result, fields, array_words):
        pass

    def get_select_fields(self):
        pass

    def hash(self, str, secret=''):
        pass

    def is_saved(self):
        pass

    def load(self, id):
        pass

    def load_on_field(self, field, value):
        pass

    def save(self):
        pass

    def search_objects(self, select, class_name, fields, search_words, min_len=3):
        pass

    def validate(self):
        pass

    def delete(self):
        pass


class passwords_dbo(base_object_db):
    pass


if __name__ == '__main__':
    log.info('Start script')
    dbo = passwords_dbo('users')
    # dbo['name_test'] = 'test'
    # dbo['name_test2'] = 'test2'
    log.debug(dbo.get_date())
