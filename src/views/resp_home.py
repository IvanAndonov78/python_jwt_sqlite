from src.services.csrf_token_service import CsrfTokenService
from src.services.user_service import UserService
from src.services.login_token_service import LoginTokenService
from src.renderers import render_header
from src.core_module import core


def resp_home(environ, response):
    if response is not None:

        user_service = UserService()
        login_token_service = LoginTokenService()

        cookies_from_browser = core.get_cookies(environ)
        csrf_token = CsrfTokenService.generate_csrf_token()
        html = ''
        # html += core.render('src/static/templates/header.html')

        input_uid_mask = input_role_mask = input_temp_token = saved_temp_token = user = role = ''
        if cookies_from_browser is not None:
            input_uid_mask += cookies_from_browser[0].split('=')[1]
            input_role_mask += cookies_from_browser[1].split('=')[1]
            input_temp_token += cookies_from_browser[2].split('=')[1]
            saved_temp_token = login_token_service.get_temp_token_by_uid_mask(input_uid_mask)
            user += user_service.get_user_by_uid_mask(input_uid_mask)
            role += user_service.get_role(user, input_role_mask)

            if user_service.is_user_logged(input_uid_mask, saved_temp_token, input_temp_token):
                html += render_header.render(1, role, csrf_token)
        else:
            html += render_header.render(0, role, csrf_token)

        html += core.render('src/static/templates/index.html')
        html += core.render('src/static/templates/footer.html')
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        response(status, headers)
        response = ''.join([html])
        return [response.encode()]

    else:
        return None

