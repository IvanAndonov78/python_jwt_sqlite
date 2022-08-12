import json
from src.services.task_service import TaskService
from src.core_module import core


def resp_ajax_tasks_search(environ, response):
    if response is not None:
        qs = environ['QUERY_STRING']
        # core.dd(qs)
        search_str = qs.split("=")[1].replace("%20", " ")
        # core.dd(search_str)
        if qs is not None:
            headers = [('Content-Type', 'application/json')]
            status = '200 OK'
            response(status, headers)

            task_service = TaskService()
            tasks = task_service.get_filtered_tasks(search_str)
            ls = []
            for row in tasks:
                dict_el = {
                    'taskid': row[0],
                    'taskname': row[1],
                    'enddate': row[2],
                    'isregular': row[3],
                    'isclosed': row[4]
                }
                ls.append(dict_el)

            response = json.dumps(ls)  # converts dict(or list of dicts) to string
            return [response.encode()]
    return None

