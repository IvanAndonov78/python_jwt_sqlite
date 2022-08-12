import json

from src.services.user_service import UserService
from src.services.login_token_service import LoginTokenService
from src.services.csrf_token_service import CsrfTokenService
from src.core_module import core


def resp_login_ajax(environ, response):
    if response is not None:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = 0

        bytes_request_body = environ['wsgi.input'].read(request_body_size)
        req_body = bytes_request_body.decode('utf8').replace("'", '"')  # str

        if req_body is not None:
            req_body_to_dict = json.loads(req_body)
            raw_input_user = req_body_to_dict['user']
            input_user = core.escape(raw_input_user)
            raw_input_pass = req_body_to_dict['password']
            input_pass = core.escape(raw_input_pass)
            input_csrf_token = req_body_to_dict['csrfToken']
            user_service = UserService()
            login_token_service = LoginTokenService()
            if CsrfTokenService.check_csrf_token(input_csrf_token) and user_service.check_user(input_user, input_pass):
                uid_mask = user_service.get_uid_mask(input_user)
                if login_token_service.save_edit_temp_token(uid_mask):
                    temp_token = login_token_service.get_temp_token_by_uid_mask(uid_mask)
                    if not temp_token:
                        return None  # TODO: create an error message response
                    resp_dict = {
                        "uid_mask": user_service.get_uid_mask(input_user),
                        "role_mask": user_service.get_role_mask(input_user),
                        "temp_token": temp_token
                    }

                    headers = [('Content-Type', 'application/json')]
                    status = '200 OK'
                    response(status, headers)
                    response = json.dumps(resp_dict)  # converts dict(or list of dicts) to string
                    return [response.encode()]
            else:
                status = '200 OK'
                headers = [('Content-type', 'text/html')]
                response(status, headers)
                msg = '<h1> Login Error! </h1>'
                response = ''.join([msg])
                return [response.encode()]
        else:
            return None


