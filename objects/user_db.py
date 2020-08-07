from abstract_object_db import *


class user_db(abstract_object_db):
    table_name = 'users'

    def __init__(self):
        super().__init__(self.table_name)


if __name__ == '__main__':
    udb = user_db()
    udb.get_all()
