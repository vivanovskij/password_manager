from base_object_db import *


class user_db(base_object_db):
    __table_name = 'users'

    def __init__(self):
        super().__init__(self.__table_name)

    def has_login(self, login):
        if self.get_row_on_field('login', login):
            return True
        else:
            return False

    def get_password(self, login):
        sql = f'SELECT `password` FROM `{self._get_table_name()}` WHERE `login` = ?'
        params = (login,)
        return self._db.select_cell(sql, params)

    def set_password(self, login, password):
        where = {'login': login}
        return self.set_value_on_field('password', password, where)

    def create_account(self, login, password):
        pass

    def auth_user(self, login, password):
        pass

    def is_auth(self):
        pass

    def logout(self):
        pass

    def delete_account(self, login):
        pass

    def get_user_id(self, name):
        pass

    def get_users(self):
        pass


if __name__ == '__main__':
    udb = user_db()
    print(udb.get_password('user1'))
