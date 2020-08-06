from db.abstract_db import *
from app_lib.config import config
from select import *


class database(abstract_db):
    __db = None

    def __init__(self, db_path=config.DB_PATH, db_prefix=config.DB_PREFIX):
        if not database.__db:
            super().__init__(db_path, db_prefix)
        else:
            self.get_dbo()

    @classmethod
    def get_dbo(cls):
        if not cls.__db:
            cls.__db = database()
        return cls.__db


if __name__ == '__main__':
    db = database.get_dbo()
    select = select(db)

    select.where('source=?', ['ВК'])
    select.sfrom('passwords', '*')
    params = {'note': 'This is something', 'user_id': '1234'}
    print(db.select(select))
