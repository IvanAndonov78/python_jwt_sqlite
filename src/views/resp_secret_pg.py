from src.core_module import core
from src.services.user_service import UserService
from src.services.login_token_service import LoginTokenService
from src.services.csrf_token_service import CsrfTokenService
from src.renderers import render_header, render_secret_page_admin, render_secret_page_visitor


def resp_secret_pg(environ, response):
    if response is not None:
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        response(status, headers)
        cookies_from_browser = core.get_cookies(environ)

        input_uid_mask = cookies_from_browser[0].split('=')[1]
        input_role_mask = cookies_from_browser[1].split('=')[1]
        input_temp_token = cookies_from_browser[2].split('=')[1]

        user_service = UserService()
        login_token_service = LoginTokenService()
        saved_temp_token = login_token_service.get_temp_token_by_uid_mask(input_uid_mask)
        csrf_token = CsrfTokenService.generate_csrf_token()

        html = ''

        if (
                user_service.is_user_logged(input_uid_mask, saved_temp_token, input_temp_token)
                and CsrfTokenService.check_csrf_token(csrf_token)
        ):
            if user_service.has_role(input_uid_mask, input_role_mask, 'Admin'):
                html += render_header.render(1, 'Admin', csrf_token)
                # html += core.render('src/static/templates/secret_page.html')
                html += render_secret_page_admin.render(csrf_token)
            elif user_service.has_role(input_uid_mask, input_role_mask, 'Visitor'):
                html += render_header.render(1, 'Admin', csrf_token)
                # html += core.render('src/static/templates/secret_page.html')
                html += render_secret_page_visitor.render()
        else:
            html += render_header.render(0, '', csrf_token)
            html += '<h1>' + 'This page requires log in!' + '</h1>'
        html += core.render('src/static/templates/footer.html')
        response = ''.join([html])
        return [response.encode()]
    else:
        return None
