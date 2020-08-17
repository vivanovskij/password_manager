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

    def get_passwords(self):
        user_id = {'user_id': self.__user.get_user_id()}
        return self._get_all_on_field(user_id)


if __name__ == '__main__':
    pdb = password_db()
    print(pdb.set_user('Алёша6', 'Ура!!!'))
    print(pdb.get_passwords())
