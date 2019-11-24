from psycopg2 import connect
from psycopg2 import Error, ProgrammingError


class InvalidRequestError(Exception):
    pass


class DBConnector:

    create_query = 'CREATE TABLE faces (' \
                   'hashcode VARCHAR(256) PRIMARY KEY ,' \
                   'emo_id VARCHAR(256) )'

    check_query = 'SELECT * FROM faces WHERE hashcode = %s'
    insert_query = 'INSERT INTO faces (hashcode, emo_id) VALUES (%s, %s)'
    get_query = 'SELECT * FROM faces'

    def __init__(self, config):
        self._dbname = config.get('DB_NAME')
        self._dbuser = config.get('DB_USER')
        self._dbhost = config.get('DB_HOST')
        self._dbpass = config.get('DB_PASS')
        self._create_table()

    def _db_connect(self):
        return connect(
            dbname=self._dbname,
            user=self._dbuser,
            host=self._dbhost,
            password=self._dbpass
        )

    def _create_table(self):
        conn = self._db_connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self.create_query)
            conn.commit()
        except ProgrammingError:
            pass
        finally:
            cursor.close()
            conn.close()

    def check_write(self, hashcode):
        conn = self._db_connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self.check_query, [hashcode, ])
            result = cursor.fetchall()
            conn.commit()
            result = result[0][1]
        except IndexError:
            result =  False
        finally:
            cursor.close()
            conn.close()
        return result

    def add_write(self, path, emo_id):
        conn = self._db_connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self.insert_query, [path, emo_id])
            conn.commit()
        except Error:
            raise InvalidRequestError
        finally:
            cursor.close()
            conn.close()

    def get_writes(self):
        conn = self._db_connect()
        cursor = conn.cursor()
        try:
            cursor.execute(self.get_query)
            result = cursor.fetchall()
            conn.commit()
        except Error:
            raise InvalidRequestError
        finally:
            cursor.close()
            conn.close()
        return result
