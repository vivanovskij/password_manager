from db.database import *
from db.base_db import *
from app_lib.logger import *
from abc import ABC
from datetime import datetime
import hashlib
from app_lib.config import config

log = logging.getLogger(__name__)


class base_object_db(ABC):
    _db = None
    __table_name = ''
    __format_date = ''

    def __init__(self, table_name):
        self._db = database.get_dbo()
        self.__table_name = table_name
        self.__format_date = config.FORMAT_DATE

    def _get_table_name(self):
        return config.DB_PREFIX + self.__table_name

    def _get_cell_on_field(self, cell, field={}):
        for k, v in field.items():
            field_name = k
            field_value = v
        sql = f'SELECT `{cell}` FROM `{self._get_table_name()}` WHERE `{field_name}`=?'
        params = (field_value,)
        return self._db.select_cell(sql, params)

    def get_date(self, date=False):
        if not date:
            date = datetime.today()
        return date.strftime(self.__format_date)

    def hash(self, string, secret=config.SALT):
        mystr = string + secret
        hash_object = hashlib.sha1(mystr.encode())
        return hash_object.hexdigest()


class passwords_dbo(base_object_db):
    pass


if __name__ == '__main__':
    pass
