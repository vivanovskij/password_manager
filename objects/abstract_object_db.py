from abc import ABC


class abstract_object_db(ABC):
    _db = None
    __format_date = ''
    __id = None
    __properties = {}
    _table_name = ''

    def __init__(self, table_name, format_date):
        self._table_name = table_name
        self._format_date = format_date

    # ability to get data like: obj.attr
    def __getitem__(self, name):
        if name == 'id':
            return self.get_id()
        if name in self.__properties:
            return self.__properties[name]['value']
        return None

    # ability to set data like: obj[attr] = value
    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __setitem__(self, name, value):
        if name in self.__properties:
            self.__properties[name]['value'] = value
            return True
        else:
            self.__setattr__(name, value)


class test_dbo(abstract_object_db):
    pass


if __name__ == '__main__':
    dbo = test_dbo('', '')
    dbo['test'] = 'This is a new attribute'
    print(dbo.test)
