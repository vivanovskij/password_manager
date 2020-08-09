from base_object_db import *


class user_db(base_object_db):
    table_name = 'users'

    def __init__(self):
        super().__init__(self.table_name)

    def has_login(self, login):
        sel = select()
        sel.sfrom(self.table_name, ('login',))
        sel.where('login=?', [login])
        row = self.__db.select(sel)
        # if


if __name__ == '__main__':
    udb = user_db()
    udb.get_all()
