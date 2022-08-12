import json

from src.core_module import core
from src.services.login_token_service import LoginTokenService


def resp_logout(environ, response):
    if response is not None:
        cookies_from_browser = core.get_cookies(environ)
        uid_mask = cookies_from_browser[0].split('=')[1]
        login_token_service = LoginTokenService()
        if uid_mask is not None or uid_mask != '':
            login_token_service.clear_token(uid_mask)
        else:
            login_token_service.clear_all_tokens()
        data = {"redirect": 1}
        headers = [('Content-Type', 'application/json')]
        status = '200 OK'
        response(status, headers)
        response = json.dumps(data)
        return [response.encode()]
    else:
        return None

