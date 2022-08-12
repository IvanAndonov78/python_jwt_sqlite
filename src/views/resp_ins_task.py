from src.services.task_service import TaskService
from src.services.csrf_token_service import CsrfTokenService
from src.core_module import core


def resp_ins_task(environ, response):
    if response is not None:
        dict_list = core.parse_req_body(environ)
        # core.dd(dict_list)

        raw_task_name = core.get_posted_input('taskname', dict_list)
        task_name = core.escape(raw_task_name)

        end_date = core.get_posted_input('enddate', dict_list)
        is_regular = core.get_posted_input('isregular', dict_list)
        is_closed = core.get_posted_input('isclosed', dict_list)
        csrf_token = core.get_posted_input('csrfToken', dict_list)

        task_service = TaskService()
        html = ''
        html += core.render('src/static/templates/header.html')
        if (
            CsrfTokenService.check_csrf_token(csrf_token)
            and task_service.insert_task(task_name, end_date, is_regular, is_closed) is not None
        ):
            html += '<h3> A new record has been saved! </h3>'
            html += '<h3> <a href="/secret"> Go Back </a> </h3>'
        else:
            html += '<h3> Something went wrong! </h3>'
        html += core.render('src/static/templates/footer.html')

        status = '200 OK'
        headers = [('Content-Type', 'text/html')]
        response(status, headers)
        response = ''.join([html])
        return [response.encode()]
    else:
        return None



