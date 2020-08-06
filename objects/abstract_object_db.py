from abc import ABC
from db.database import *
from db.abstract_db import *
# from database import database
# from abstract_db import abstract_db


class abstract_object_db(ABC):
    _db = None
    __id = None
    __properties = {}
    _table_name = ''

    def __init__(self, table_name):
        self._table_name = table_name
        self._db = database.get_dbo()

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

    def add_property(self, field, default=None, validator=None):
        # self.__properties[field] = {'value': default, 'validator': validator}
        pass

    @classmethod
    def add_sub_object(cls, data, class_name, field_out, field_in):
        # ids = [cls.get_complex_value(value, field_in) for value in data]
        pass

    @classmethod
    def get_complex_value(cls, obj, field):
        if '.' in field:
            field = split('.')
        if isinstance(field, (list, tuple)):
            value = obj
            for f in field:
                value = value[f]
        else:
            value = obj[field]
        return value

    def build_multiple(self, class_name, data):
        pass

    def compare_relevant(self, value1, value2):
        pass

    def delete(self):
        pass

    def get_all(self):
        pass

    def get_all_on_field(self):
        pass

    def get_all_on_ids(self, ids):
        pass

    def get_all_on_ids_field(self, ids, field):
        pass

    def get_all_on_where(self, table_name, where=False, values=False, order=False, ask=True, count=False, offset=False):
        pass

    def get_all_with_order(self, table_name, order, ask=True, count=False, offset=False):
        pass

    def get_base_select(self, table_name):
        pass

    def get_date(self, date=False):
        pass

    def get_id(self):
        pass

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

    def set_db(self, db):
        pass

    def validate(self):
        pass


class test_dbo(abstract_object_db):
    pass


if __name__ == '__main__':
    dbo = test_dbo('')
    dbo['test'] = 'This is a new attribute'
    dbo['another'] = 'This is another attribute'
    print(dbo.test, dbo.another)
