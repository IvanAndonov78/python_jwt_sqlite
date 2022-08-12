import math

from src.models.conn_dao import ConnDao
from src.core_module import core


class PaginationService(ConnDao):
    def __init__(self, items_per_page=None):
        ConnDao.__init__(self)
        self.db_conn = super().get_connection()
        self.items_per_page = items_per_page

    def get_total_items(self):
        cursor = self.conn.cursor()
        sql_query = "SELECT COUNT(task.taskid) FROM task"
        cursor.execute(sql_query)
        count = cursor.fetchone()[0]
        self.conn.commit()
        self.conn.close()
        return count

    def get_pages(self):
        total_items = self.get_total_items()
        # pages = int(round(total_items/self.items_per_page))
        pages = int(math.ceil(total_items/self.items_per_page))
        if pages > 0:
            return pages
        else:
            return 0

    def paginate(self, page_num):
        start = 0
        if int(page_num) > 1:
            start = (page_num * self.items_per_page) - self.items_per_page

        connection = self.db_conn
        cursor = connection.cursor()

        # sql = "SELECT * FROM `cash_receipt_notes` LIMIT 4 OFFSET 0";
        # sql = "SELECT * FROM `cash_receipt_notes` LIMIT 0, 4"; # the same
        sql_query = f"SELECT * FROM task LIMIT {self.items_per_page} OFFSET {start}"
        tasks = []
        for row in cursor.execute(sql_query):
            tasks.append(row)

        connection.commit()
        connection.close()
        return tasks


