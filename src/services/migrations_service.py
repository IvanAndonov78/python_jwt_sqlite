from src.core_module import core
from src.services.task_service import TaskService
from src.services.user_service import UserService
from src.services.login_token_service import LoginTokenService
from src.models.conn_dao import ConnDao


class MigrationsService:
    def __init__(self):
        pass

    # @classmethod
    # def step1_print_all_db_tables(cls):
    #     conn_dao = ConnDao()
    #     connection = conn_dao.get_connection()
    #     cursor = connection.cursor()
    #     sql = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
    #     print('-- Step 1 START: Print all DB Tables: ------------------------')
    #     for row in cursor.execute(sql):
    #         core.dd(row)
    #     connection.commit()
    #     connection.close()
    #    print('-- Step 1 END: -----------------------------------------------')

    @classmethod
    def step2_print_recs_in_user_table(cls):
        user_service = UserService()
        print('-- Step 2 START: Print Records in "user" Table: --------------')
        users = user_service.get_all_users()
        for row in users:
            core.dd(row)
        print('-- Step 2 END: -----------------------------------------------')

    @classmethod
    def step3_print_recs_in_login_token_table(cls):
        login_token_service = LoginTokenService()
        print('-- Step 3 START: Print Records in "login_token" Table: -------')
        login_tokens = login_token_service.get_login_tokens()
        for row in login_tokens:
            core.dd(row)
        print('-- Step 3 END: -----------------------------------------------')

    @classmethod
    def step4_print_recs_in_task_table(cls):
        task_service = TaskService()
        print('-- Step 4 START: Print Records in Task Table: ----------------')
        tasks = task_service.get_all_tasks()
        for row in tasks:
            core.dd(row)
        print('-- Step 4 END: -----------------------------------------------')

    @classmethod
    def print_db_data(cls):
        # cls.step1_print_all_db_tables()  # task, user, login_token
        cls.step2_print_recs_in_user_table()
        cls.step3_print_recs_in_login_token_table()
        cls.step4_print_recs_in_task_table()

    @classmethod
    def delete_all_db_tables(cls):
        user_service = UserService()
        login_token_service = LoginTokenService()
        task_service = TaskService()
        steps = []
        if user_service.delete_table_user():
            steps.append('Table "user" has been deleted!')
            if login_token_service.delete_table_login_token():
                steps.append('Table "login_token" has been deleted')
                if task_service.delete_table_task():
                    steps.append('Table "login_token" has been deleted')
        print('--------------------------------------')
        for el in steps:
            print(el)
        print('--------------------------------------')
        if len(steps) == 3:
            print('All DB Tables have been deleted!')
            print('--------------------------------------')
            return True
        print('SOMETHING WENT WRONG!')
        return False

    @classmethod
    def create_all_db_tables(cls):
        user_service = UserService()
        login_token_service = LoginTokenService()
        task_service = TaskService()
        steps = []
        print('--------------------------------------')
        if user_service.create_table_user():
            steps.append('Table "user" has been created!')
            if login_token_service.create_table_login_token():
                steps.append('Table "login_token" has been created!')
                if task_service.create_table_task():
                    steps.append('Table "task" has been created!')
        print('--------------------------------------')
        for el in steps:
            print(el)
        print('--------------------------------------')
        if len(steps) == 3:
            print('All DB Tables have been created!')
            print('--------------------------------------')
            return True
        print('SOMETHING WENT WRONG!')
        return False

    @classmethod
    def job_some_tasks_insert(cls):
        task_service = TaskService()
        counter = 0
        for i in range(1, 22, 1):
            task_name = f"Test task {i}"
            if task_service.insert_task(task_name, '2022-07-27', 0, 1):
                counter += 1
        if counter == 21:
            return True
        return False

    @classmethod
    def migrate_data(cls):
        user_service = UserService()
        login_token_service = LoginTokenService()

        steps = []
        print('--------------------------------------')
        if user_service.migrate_users():
            steps.append('Users Data have been inserted!')
            if login_token_service.migrate_empty_tokens():
                steps.append('Login Tokens (empty) Data have been inserted!')
                if cls.job_some_tasks_insert():
                    steps.append('Tasks Data have been inserted!')
        print('--------------------------------------')
        for el in steps:
            print(el)
        print('--------------------------------------')
        if len(steps) == 3:
            print('All Data have been migrated!')
            print('--------------------------------------')
            return True
        print('SOMETHING WENT WRONG!')
        return False
