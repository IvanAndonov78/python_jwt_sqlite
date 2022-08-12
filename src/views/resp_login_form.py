from src.core_module import core
from src.services.csrf_token_service import CsrfTokenService
from src.renderers import render_header, render_login_form


def resp_login_form(response):
    if response is not None:
        csrf_token = CsrfTokenService.generate_csrf_token()
        html = ''
        # html += core.render('src/static/templates/header.html')
        html += render_header.render('', '', csrf_token)
        html += render_login_form.render(csrf_token)
        html += core.render('src/static/templates/footer.html')
        status = '200 OK'
        headers = [('Content-type', 'text/html')]
        response(status, headers)
        response = ''.join([html])
        return [response.encode()]
    else:
        return None

