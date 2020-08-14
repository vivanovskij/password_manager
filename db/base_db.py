from app_lib.logger import *
import sqlite3

log = logging.getLogger(__name__)


class base_db():
    __db = None
    __cursor = None
    __prefix = ''

    def __init__(self, db_path='', db_prefix=''):
        # Prefix for database
        self.__prefix = db_prefix

        # Connect to database
        try:
            self.__db = sqlite3.connect(db_path)
        except sqlite3.DatabaseError as err:
            log.error('Error connection to database')
        else:
            self.__cursor = self.__db.cursor()

    def __del__(self):
        self.__db.close()

    def get_cursor(self):
        return self.__cursor

    def __execute(self, query, params):
        try:
            result = self.__cursor.execute(query, params)
        except sqlite3.DatabaseError as err:
            log.error(err)
            return False
        return result

    def query(self, query, params=None):
        if self.__execute(query, params):
            self.__db.commit()
            return True
        else:
            return False

    def select_all(self, query, params):
        result = self.__execute(query, params).fetchall()
        if not result:
            return False
        return result

    def select_row(self, query, params):
        result = self.__execute(query, params).fetchone()
        if not result:
            return False
        return result

    def select_cell(self, query, params):
        result = self.__execute(query, params).fetchone()
        if not result:
            return False
        else:
            return result[0]

    def insert(self, table_name, row):
        if len(row) == 0:
            return False
        fields = '('
        values = 'VALUES ('
        params = []
        for key, value in row.items():
            fields += f'`{key}`,'
            values += '?,'
            params.append(value)
        fields = fields[:-1]
        values = values[:-1]
        fields += ')'
        values += ')'
        query = f'INSERT INTO `{table_name}` {fields} {values}'
        log.debug(f'insert: {query}')
        return self.query(query, params)

    # param fields - dict {'field': 'value'}
    # param where - dict {'field': 'value'}
    def update(self, table_name, fields={}, where=False):
        if len(fields) == 0:
            return False
        query = f'UPDATE `{table_name}` SET '
        params = []
        for field, value in fields.items():
            query += f'`{field}` = ?,'
            params.append(value)
        query = query[:-1]
        if where:
            for field, value in where.items():
                query += f' WHERE `{field}` = ?'
                params.append(value)
                break
        log.debug(f'update: {query}')
        return self.query(query, params)

    def delete(self, table_name, where=False):
        table_name = self.get_table_name(table_name)
        query = f'DELETE FROM `{table_name}`'
        params = None
        if where:
            query += f' {where.get_where()}'
            params = where.get_where_params()
        log.debug(f'delete: {query}')
        return self.query(query, params)


class test_db(base_db):
    pass


if __name__ == '__main__':
    pass
