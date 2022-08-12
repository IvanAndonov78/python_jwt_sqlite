import json

from src.services.task_service import TaskService
from src.services.csrf_token_service import CsrfTokenService
from src.core_module import core


def resp_ajax_ins_task(environ, response):
    if response is not None:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0

        bytes_request_body = environ['wsgi.input'].read(request_body_size)
        req_body = bytes_request_body.decode('utf8').replace("'", '"')  # str

        if req_body is not None:
            req_body_to_dict = json.loads(req_body)
            raw_task_name = req_body_to_dict['taskname']
            task_name = core.escape(raw_task_name)
            end_date = req_body_to_dict['enddate']
            is_regular = int(req_body_to_dict['isregular'])
            is_closed = int(req_body_to_dict['isclosed'])
            csrf_token = req_body_to_dict['csrfToken']
            # core.dd(req_body_to_dict)
            task_service = TaskService()
            if (
                task_service.insert_task(task_name, end_date, is_regular, is_closed) is not None
                and CsrfTokenService.check_csrf_token(csrf_token)
            ):
                headers = [('Content-Type', 'application/json')]
                status = '200 OK'
                response(status, headers)
                resp_dict = {
                    "success_msg": "A new record has been saved!"
                }
                response = json.dumps(resp_dict)  # converts dict(or list of dicts) to string
                return [response.encode()]
    return None

