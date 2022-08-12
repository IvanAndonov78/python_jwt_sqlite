import json

from src.services.task_service import TaskService
from src.services.csrf_token_service import CsrfTokenService
from src.core_module import core


def resp_ajax_edit_task(environ, response):
    if response is not None:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0

        bytes_request_body = environ['wsgi.input'].read(request_body_size)
        req_body = bytes_request_body.decode('utf8').replace("'", '"')  # str

        if req_body is not None:
            req_body_to_dict = json.loads(req_body)
            task_id = int(req_body_to_dict['taskid'])
            raw_task_name = req_body_to_dict['taskname']
            task_name = core.escape(raw_task_name)
            end_date = req_body_to_dict['enddate']
            is_regular = int(req_body_to_dict['isregular'])
            is_closed = int(req_body_to_dict['isclosed'])
            csrf_token = req_body_to_dict['csrfToken']

            task_service = TaskService()
            if (
                task_service.edit_task(task_id, task_name, end_date, is_regular, is_closed) is not None
                and CsrfTokenService.check_csrf_token(csrf_token)
            ):
                headers = [('Content-Type', 'application/json')]
                status = '200 OK'
                response(status, headers)
                resp_dict = {
                    "taskID": task_id
                }
                response = json.dumps(resp_dict)  # converts dict(or list of dicts) to string
                return [response.encode()]
    return None



