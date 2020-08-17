from base_object_db import *
from user_db import *

log = logging.getLogger(__name__)


class password_db(base_object_db):
    __table_name = 'passwords'
    __user = None

    def __init__(self):
        super().__init__(self.__table_name)
        self.__user = user_db()

    def set_user(self, login, password):
        if self.__user.auth_user(login, password):
            return True
        else:
            return False

    def get_registrations(self):
        user_id = {'user_id': int(self.__user.get_user_id())}
        try:
            result = self._get_all_on_field(user_id)
        except Exception as err:
            log.error(err)
            return False
        return result

    def new_source(self, source, login, password, note):
        #??? вставить проверку на существование ресурса
        row = {
            'source': source,
            'login': login,
            'password': self.hash(password),
            'note': note,
            'user_id': self.__user.get_user_id(),
            'create_date': self._get_date()
        }
        return self._insert_row(row)

    def update_source(self, source, login, password, note):
        #??? вставить проверку на существование ресурса
        row = {
            'login': login,
            'password': self.hash(password),
            'note': note,
            'create_date': self._get_date()
        }
        return self._update_row_on_field(row, {'source': source})

    def delete_source(self, source):
        return self._delete_row({'source': source})


if __name__ == '__main__':
    pdb = password_db()
    print(pdb.set_user('Алёша6', 'Ура!!!'))
    pdb.new_source('One', 'Two', 'Three', 'Four')
    print(pdb.get_registrations())
    # pdb.delete_source('One')
    # print(pdb.get_registrations())
    pdb.update_source('One', 'Два', 'Три', 'Четыре')
    print(pdb. get_registrations())
