import random
import string

from src.models.conn_dao import ConnDao
from src.services.user_service import UserService
from src.core_module import core


class LoginTokenService(ConnDao):
    def __init__(self, uid_mask=None, temp_token=None):
        self.uid_mask = uid_mask
        self.temp_token = temp_token

    def create_table_login_token(self):
        connection = self.conn  # inherited from the parent ConnDao
        cursor = connection.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS login_token (
                uidmask TEXT, 
                temptoken TEXT NOT NULL
            )
        """
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return True

    def list_all_db_tables(self):
        connection = self.conn
        cursor = connection.cursor()
        sql = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
        for row in cursor.execute(sql):
            core.dd(row)
        self.conn.commit()
        self.conn.close()

    def delete_table_login_token(self):
        connection = self.conn
        cursor = connection.cursor()
        sql = "DROP TABLE IF EXISTS login_token"
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def generate_token():
        first = string.ascii_letters
        letters = ''.join(random.choice(first) for i in range(10))

        second = string.digits
        digits = ''.join(random.choice(second) for i in range(10))

        list_sp_symbols = ['^', '!', '~']
        sp_symbols = ''.join(list_sp_symbols)

        pre_token = letters + str(digits) + str(sp_symbols)
        token = ''.join(random.sample(pre_token, len(pre_token)))

        return token

    @staticmethod
    def save_edit_temp_token(uid_mask):
        conn_dao = ConnDao()
        connection = conn_dao.get_connection()
        cursor = connection.cursor()
        temp_token = LoginTokenService.generate_token()
        sql_params = (temp_token, uid_mask)
        sql = "UPDATE login_token SET temptoken = :temp_token WHERE uidmask = :uid_mask;"
        cursor.execute(sql, sql_params)
        connection.commit()
        connection.close()
        # return cursor.lastrowid
        if cursor.lastrowid is not None:
            return True
        return False

    @staticmethod
    def save_empty_token(uid_mask):
        conn_dao = ConnDao()
        connection = conn_dao.get_connection()
        cursor = connection.cursor()
        temp_token = ""
        sql_params = (uid_mask, temp_token)
        sql = """
                    INSERT into login_token 
                    (uidmask, temptoken)
                    VALUES 
                    (:uid_mask, :temp_token)
                """
        cursor.execute(sql, sql_params)
        connection.commit()
        connection.close()
        return cursor.lastrowid

    def get_temp_token_by_uid_mask(self, uid_mask):
        cursor = self.conn.cursor()
        sql_params = (uid_mask,)
        sql_query = "SELECT lt.temptoken FROM login_token as lt WHERE lt.uidmask = :uid_mask;"
        cursor.execute(sql_query, sql_params)
        login_token = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return login_token

    def get_login_tokens(self):
        cursor = self.conn.cursor()
        login_tokens = []
        sql = "SELECT * from login_token;"
        for row in cursor.execute(sql):
            login_tokens.append(row)
        self.conn.commit()
        self.conn.close()
        return login_tokens

    def migrate_empty_tokens(self):
        user_service = UserService()
        users = user_service.get_conf_users()
        counter = 0
        for i in range(0, len(users), 1):
            uid_mask = user_service.get_uid_mask_by_conf_pos(i)
            if self.save_empty_token(uid_mask) is not None:
                counter += 1
        if counter == len(users):
            return True
        return False

    @staticmethod
    def edit_login_token(uid_mask, temp_token):
        conn_dao = ConnDao()
        connection = conn_dao.get_connection()
        cursor = connection.cursor()
        sql_params = (uid_mask, temp_token)  # REORDED items as in sql!
        sql = """
                UPDATE login_token SET 
                temptoken = :temp_token 
                WHERE uidmask = :uid_mask
                """
        cursor.execute(sql, sql_params)
        connection.commit()
        connection.close()
        return cursor.lastrowid

    @staticmethod
    def del_all_login_tokens():
        conn_dao = ConnDao()
        connection = conn_dao.get_connection()
        cursor = connection.cursor()
        sql = 'DELETE FROM login_token;'
        cursor.execute(sql)
        connection.commit()
        return True

    def clear_token(self, uid_mask):
        self.edit_login_token(uid_mask, "")

    def clear_all_tokens(self):
        self.del_all_login_tokens()







