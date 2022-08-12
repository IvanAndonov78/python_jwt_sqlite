from src.models.conn_dao import ConnDao
from src.core_module import core


class TaskService(ConnDao):
    def __init__(self, task_name=None, end_date=None, is_regular=None, is_closed=None):
        ConnDao.__init__(self)  # == super().__init__(self)
        self.task_name = task_name
        self.end_date = end_date
        self.is_regular = is_regular
        self.is_closed = is_closed

    def create_table_task(self):
        connection = self.conn  # inherited from the parent ConnDao
        cursor = connection.cursor()
        sql = """
            CREATE TABLE IF NOT EXISTS task (
                taskid INTEGER PRIMARY KEY AUTOINCREMENT, 
                taskname TEXT NOT NULL,
                enddate TEXT NOT NULL,
                isregular INTEGER NOT NULL,
                isclosed INTEGER NOT NULL
            )
        """
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return True

    def delete_table_task(self):
        connection = self.conn
        cursor = connection.cursor()
        sql = "DROP TABLE IF EXISTS task"
        cursor.execute(sql)
        connection.commit()
        connection.close()
        return True

    @staticmethod
    def insert_task(task_name, end_date, is_regular, is_closed):
        conn_dao = ConnDao()
        connection = conn_dao.get_connection()
        cursor = connection.cursor()
        task = (task_name, end_date, is_regular, is_closed)
        sql = """
                INSERT into task 
                (taskname, enddate, isregular, isclosed)
                VALUES 
                (:task_name, :end_date, :is_regular, :is_closed)
            """
        cursor.execute(sql, task)
        connection.commit()
        connection.close()
        # return cursor.lastrowid
        if cursor.lastrowid is not None:
            return True
        return False

    @staticmethod
    def del_task(task_id):
        conn_dao = ConnDao()
        connection = conn_dao.get_connection()
        cursor = connection.cursor()
        sql_params = (task_id,)
        sql = 'DELETE FROM task WHERE taskid = :task_id'
        cursor.execute(sql, sql_params)
        connection.commit()
        return True

    @staticmethod
    def edit_task(task_id, task_name, end_date, is_regular, is_closed):
        conn_dao = ConnDao()
        connection = conn_dao.get_connection()
        cursor = connection.cursor()
        sql_params = (task_name, end_date, is_regular, is_closed, task_id)  # REORDED items as in sql!
        sql = """
            UPDATE task SET 
            taskname = :task_name, 
            enddate = :end_date, 
            isregular = :is_regular, 
            isclosed = :is_closed
            WHERE taskid = :task_id
            """

        cursor.execute(sql, sql_params)
        connection.commit()
        connection.close()
        return cursor.lastrowid

    def get_all_tasks(self):
        cursor = self.conn.cursor()
        tasks = []
        select_query = "SELECT * from task"
        for row in cursor.execute(select_query):
            tasks.append(row)

        self.conn.commit()
        self.conn.close()
        return tasks

    def get_filtered_tasks(self, search_str):
        cursor = self.conn.cursor()
        tasks = []
        select_query = "SELECT * from task "
        select_query += f"WHERE taskname LIKE '{'%' + search_str + '%'}'"
        select_query += f" OR enddate LIKE '{'%' + search_str + '%'}'"
        # core.dd(select_query)
        for row in cursor.execute(select_query):
            tasks.append(row)

        self.conn.commit()
        self.conn.close()
        return tasks
