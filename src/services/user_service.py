import json
from src.models.conn_dao import ConnDao
from src.core_module import core


class UserService(ConnDao):
    def __init__(self, user=None, password=None, role=None, is_active=None, uid_mask=None, role_mask=None):
        ConnDao.__init__(self)  # == super().__init__(self)
        self.user = user
        self.password = password
        self.role = role
        self.is_active = is_active
        self.uid_mask = uid_mask
        self.role_mask = role_mask

    def list_all_db_tables(self):
        connection = self.conn
        cursor = connection.cursor()
        sql = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
        for row in cursor.execute(sql):
            core.dd(row)
        self.conn.commit()
        self.conn.close()

    def create_table_user(self):
        connection = self.conn  # inherited from the parent ConnDao
        cursor = connection.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS user (
                user TEXT UNIQUE, 
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                isactive INTEGER NOT NULL,
                uidmask TEXT NOT NULL,
                rolemask TEXT NOT NULL
            )
        """
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return True

    def delete_table_user(self):
        connection = self.conn
        cursor = connection.cursor()
        sql = "DROP TABLE IF EXISTS user"
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def get_conf_users():
        with open('src/conf/users_migrations.json') as data_file:
            dict_data = json.load(data_file)
        return dict_data['users']  # list

    def get_user_by_conf_pos(self, posIdx):
        data = self.get_conf_users()
        return data[posIdx]['user']

    def get_password_by_conf_pos(self, posIdx):
        data = self.get_conf_users()
        return data[posIdx]['password']

    def get_role_by_conf_pos(self, posIdx):
        data = self.get_conf_users()
        return data[posIdx]['role']

    def get_is_active_by_conf_pos(self, posIdx):
        data = self.get_conf_users()
        return data[posIdx]['isactive']

    def get_uid_mask_by_conf_pos(self, posIdx):
        data = self.get_conf_users()
        return data[posIdx]['uidmask']

    def get_role_mask_by_conf_pos(self, posIdx):
        data = self.get_conf_users()
        return data[posIdx]['rolemask']

    @staticmethod
    def insert_user(user, password, role, is_active, uid_mask, role_mask):
        conn_dao = ConnDao()
        connection = conn_dao.get_connection()
        cursor = connection.cursor()
        sql_params = (user, password, role, is_active, uid_mask, role_mask)
        sql = """
                INSERT into user 
                (user, password, role, isactive, uidmask, rolemask)
                VALUES 
                (:user, :password, :role, :is_active, :uid_mask, :role_mask)
            """
        cursor.execute(sql, sql_params)
        connection.commit()
        connection.close()
        return cursor.lastrowid

    @staticmethod
    def edit_user(password, role, is_active, uid_mask, role_mask, uid):
        conn_dao = ConnDao()
        connection = conn_dao.get_connection()
        cursor = connection.cursor()
        sql_params = (password, role, is_active, uid_mask, role_mask, uid)  # REORDED items as in sql!
        sql = """
            UPDATE user SET 
            password = :password, 
            role = :role, 
            isactive = :is_active,
            uidmask = :uid_mask, 
            rolemask = :role_mask 
            WHERE user = :uid
            """
        cursor.execute(sql, sql_params)
        connection.commit()
        connection.close()
        return cursor.lastrowid

    @staticmethod
    def del_user(uid):
        conn_dao = ConnDao()
        connection = conn_dao.get_connection()
        cursor = connection.cursor()
        sql_params = (uid,)
        sql = 'DELETE FROM user WHERE user = :uid'
        cursor.execute(sql, sql_params)
        connection.commit()
        return True

    def get_role(self, user_name, role_mask):
        cursor = self.conn.cursor()
        sql_params = (user_name, role_mask)
        sql_query = "SELECT u.role FROM user as u WHERE u.user = :user_name and u.rolemask = :role_mask;"
        cursor.execute(sql_query, sql_params)
        role = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return role

    def migrate_users(self):
        users = self.get_conf_users()
        counter = 0
        for i in range(0, len(users), 1):
            user = self.get_user_by_conf_pos(i)
            password = self.get_password_by_conf_pos(i)
            role = self.get_role_by_conf_pos(i)
            is_active = self.get_is_active_by_conf_pos(i)
            uid_mask = self.get_uid_mask_by_conf_pos(i)
            role_mask = self.get_role_mask_by_conf_pos(i)
            if self.insert_user(user, password, role, is_active, uid_mask, role_mask) is not None:
                counter += 1
        if counter == len(users):
            return True
        return False

    def get_users_from_db(self):
        cursor = self.conn.cursor()
        users = []
        sql = "SELECT * from user;"
        # core.dd(sql)
        for row in cursor.execute(sql):
            users.append(row)
        self.conn.commit()
        self.conn.close()
        return users

    def get_saved_user(self, input_username):
        cursor = self.conn.cursor()
        sql_params = (input_username,)
        sql_query = "SELECT u.user FROM user as u WHERE u.user = :input_username;"
        cursor.execute(sql_query, sql_params)
        user = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return user

    def get_user_by_uid_mask(self, input_uid_mask):
        cursor = self.conn.cursor()
        sql_params = (input_uid_mask,)
        sql_query = "SELECT u.user FROM user as u WHERE u.uidmask = :input_uid_mask;"
        cursor.execute(sql_query, sql_params)
        user = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return user

    def get_saved_password(self, input_username, input_password):
        cursor = self.conn.cursor()
        sql_params = (input_username, input_password,)
        sql_query = "SELECT u.password FROM user as u where u.user = :input_username AND u.password = :input_password;"
        cursor.execute(sql_query, sql_params)
        password = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return password

    def is_active_user(self, input_username):
        cursor = self.conn.cursor()
        sql_params = (input_username,)
        sql_query = "SELECT u.isactive FROM user as u where u.user = :input_username;"
        cursor.execute(sql_query, sql_params)
        is_active = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        if is_active == 1:
            return True
        return False

    def get_uid_mask(self, input_username):
        cursor = self.conn.cursor()
        sql_params = (input_username,)
        sql_query = "SELECT u.uidmask FROM user as u where u.user = :input_username;"
        cursor.execute(sql_query, sql_params)
        uid_mask = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return uid_mask

    def get_role_mask(self, input_username):
        cursor = self.conn.cursor()
        sql_params = (input_username,)
        sql_query = "SELECT u.rolemask FROM user as u where u.user = :input_username;"
        cursor.execute(sql_query, sql_params)
        role_mask = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return role_mask

    def check_user(self, input_username, input_password):
        if self.get_saved_user(input_username) == input_username:
            if self.get_saved_password(input_username, input_password) == input_password:
                if self.is_active_user(input_username):
                    return True
        return False

    def get_user_by_uid_mask(self, input_user_mask):
        cursor = self.conn.cursor()
        sql_params = (input_user_mask,)
        sql_query = "SELECT u.user FROM user as u where u.uidmask = :input_user_mask;"
        cursor.execute(sql_query, sql_params)
        user = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return user

    def get_all_users(self):
        cursor = self.conn.cursor()
        users = []
        select_query = "SELECT * from user"
        for row in cursor.execute(select_query):
            users.append(row)

        self.conn.commit()
        self.conn.close()
        return users

    def is_user_logged(self, input_uid_mask, saved_temp_token, input_temp_token):
        saved_user = self.get_user_by_uid_mask(input_uid_mask)
        if self.is_active_user(saved_user) and saved_temp_token == input_temp_token:
            return True
        return False

    def has_role(self, input_uid_mask, input_role_mask, input_role_name):
        saved_user = self.get_user_by_uid_mask(input_uid_mask)
        saved_role = self.get_role(saved_user, input_role_mask)
        if saved_role == input_role_name:
            return True
        return False






