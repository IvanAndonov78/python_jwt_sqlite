import json

from src.services.task_service import TaskService


def resp_ajax_del_task(environ, response):
    if response is not None:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0

        bytes_request_body = environ['wsgi.input'].read(request_body_size)
        req_body = bytes_request_body.decode('utf8').replace("'", '"')  # str

        if req_body is not None:
            req_body_to_dict = json.loads(req_body)
            task_id = req_body_to_dict['taskid']
            task_service = TaskService()
            if task_service.del_task(task_id):
                headers = [('Content-Type', 'application/json')]
                status = '200 OK'
                response(status, headers)
                resp_dict = {
                    "taskID": task_id
                }
                response = json.dumps(resp_dict)  # converts dict(or list of dicts) to string
                return [response.encode()]
    return None

