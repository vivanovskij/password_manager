from base_object_db import *


class user_db(base_object_db):
    __table_name = 'users'
    __user_id = None

    def __init__(self):
        super().__init__(self.__table_name)

    def has_login(self, login):
        if self._get_cell_on_field('login', {'login': login}):
            return True
        else:
            return False

    def get_password(self, login):
        return self._get_cell_on_field('password', {'login': login})

    def set_password(self, login, password):
        password = self.hash(password)
        update = {'password': password}
        where = {'login': login}
        return self._db.update(self._get_table_name(), update, where)

    def _check_password(self, login, password):
        return self.get_password(login) == self.hash(password)

    def create_account(self, login, password):
        if self.has_login(login):
            log.warning('Login exist')
            return False
        password = self.hash(password)
        date = self._get_date()
        row = {'login': login,
               'password': password,
               'create': date}
        try:
            self._insert_row(row)
        except:
            return False
        else:
            return True

    def auth_user(self, login, password):
        if self.has_login(login) and self._check_password(login, password):
            self.__user_id = self._get_cell_on_field('id', {'login': login})
            return True
        else:
            return False

    def is_auth(self):
        if self.__user_id:
            return True
        else:
            return False

    def get_user_id(self):
        if self.is_auth():
            return self.__user_id
        else:
            return None

    def logout(self):
        if self.is_auth():
            self.__user_id = None

    def delete_account(self, login):
        self.logout()
        try:
            self._delete_row({'login': login})
        except:
            return False
        else:
            return True

    def get_users(self):
        try:
            result = self._get_column('login')
        except:
            return False
        else:
            return result


if __name__ == '__main__':
    udb = user_db()
    # udb.create_account('Алёша6', 'Ура!!!')
    print(udb.get_users())
