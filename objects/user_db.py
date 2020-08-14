from base_object_db import *


class user_db(base_object_db):
    __table_name = 'users'

    def __init__(self):
        super().__init__(self.__table_name)

    def has_login(self, login):
        if self._get_cell_on_field('login', {'login': login}):
            return True
        else:
            return False

    def get_password(self, login):
        # вынести в базовый класс???
        # self._get_cell_on_field()

        return self._get_cell_on_field('password', {'login': login})

    def set_password(self, login, password):
        password = self.hash(password)
        update = {'password': password}
        where = {'login': login}
        return self._db.update(self._get_table_name(), update, where)

    def create_account(self, login, password):
        if self.has_login(login):
            log.warning('Login exist')
            return False
        password = self.hash(password)
        date = datetime.now().strftime(config.FORMAT_DATE)
        row = {'login': login,
               'password': password,
               'create': date}
        return self._db.insert(self._get_table_name(), row)

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
    # print(udb.get_password('Алёша'))
    # print(udb.has_login('Алёша'))
    # print(udb.set_password('Алёша', 'qwertys'))
    # print(udb.get_password('Алёша'))
    print(udb.create_account('Алёша5', 'Ура!!!'))
