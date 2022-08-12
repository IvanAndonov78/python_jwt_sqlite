import json
from src.services.task_service import TaskService
from src.services.pagination_service import PaginationService


def resp_ajax_tasks(response):
    if response is not None:
        headers = [('Content-Type', 'application/json')]
        status = '200 OK'
        response(status, headers)

        task_service = TaskService()
        tasks = task_service.get_all_tasks()

        paginator = PaginationService(5)
        pages = paginator.get_pages()  # total pages

        ls = []
        for row in tasks:
            dict_el = {
                'taskid': row[0],
                'taskname': row[1],
                'enddate': row[2],
                'isregular': row[3],
                'isclosed': row[4],
                'total_pages': pages
            }
            ls.append(dict_el)

        response = json.dumps(ls)  # converts dict(or list of dicts) to string
        return [response.encode()]
    else:
        return None

