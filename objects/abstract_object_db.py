from abc import ABC
from db.database import *
from db.abstract_db import *
from db.select import *
from app_lib.logger import *

log = logging.getLogger(__name__)


class abstract_object_db(ABC):
    db = None
    table_name = 'users'
    __properties = {}
    __id = None

    def __init__(self, table_name):
        self.db = database.get_dbo()
        self.table_name = table_name

    # ability to get data like: obj.attr
    def __get__(self, name):
        if name == 'id':
            return self.get_id()
        if name in self.__properties:
            return self.__properties[name]['value']
        return None

    # ability to set data like: obj[attr]=value

    def __setitem__(self, name, value):
        if name in self.__properties:
            self.__properties[name]['value'] = value
            return True
        else:
            self.__dict__[name] = value

    def add_property(self, field, validator=None, default=None):
        self.__properties[field] = {'value': default, 'validator': validator}

    @classmethod
    def add_sub_object(cls, data, class_name, field_out, field_in):
        # ids = [cls.get_complex_value(value, field_in) for value in data]
        pass

    @classmethod
    def get_complex_value(cls, obj, field):
        if '.' in field:
            field = split('.')
        if isinstance(field, (list, tuple, dict)):
            value = obj
            for f in field:
                value = value[f]
        else:
            value = obj[field]
        return value

    def build_multiple(self, cls, data):
        ret = {}
        log.debug(data)
        for row in data:
            obj = cls.__new__(cls)
            obj.init(row)
            key = obj.get_id()
            value = obj
            ret.update({key: value})
        return ret

    def compare_relevant(self, value1, value2):
        pass

    def delete(self):
        pass

    def get_all(self, count=False, offset=False):
        return self.get_all_with_order(self.table_name, self.__class__, 'id', True, count, offset)

    def get_all_on_field(self):
        pass

    def get_all_on_ids(self, ids):
        pass

    def get_all_on_ids_field(self, ids, field):
        pass

    def get_all_on_where(self, table_name, cls, where=False, values=False, order=False, ask=True, count=False, offset=False):
        sel = select()
        sel.sfrom(table_name, '*')
        if where:
            sel.where(where, values)
        if order:
            sel.order(order, ask)
        else:
            sel.order('id')
        if count:
            sel.limit(count, offset)
        data = self.db.select(sel)
        return self.build_multiple(self.__class__, data)

    def get_all_with_order(self, table_name, cls, order, ask=True, count=False, offset=False):
        return self.get_all_on_where(table_name, cls, False, False, order, ask, count, offset)

    def get_base_select(self, table_name):
        pass

    def get_date(self, date=False):
        pass

    def get_id(self):
        return int(self.__id)

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

    def init(self, row):
        for key, value in self.__properties.items():
            val = row[key]
            self.__properties[key]['value'] = val
        log.debug(row)
        self.id = row[0]
        return True

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

    def set_db(self, db):
        pass

    def validate(self):
        pass


class passwords_dbo(abstract_object_db):
    pass


if __name__ == '__main__':
    log.info('Start script')
    dbo = passwords_dbo('passwords')
    dbo.get_all()
