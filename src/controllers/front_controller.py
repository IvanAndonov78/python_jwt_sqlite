from src.views.resp_favicon import resp_favicon
from src.views.resp_not_found import resp_not_found
from src.views.resp_main_css import resp_main_css
from src.views.resp_auth_service_js import resp_auth_service_js
from src.views.resp_home import resp_home
from src.views.resp_login_form import resp_login_form
from src.views.resp_secret_pg import resp_secret_pg
from src.views.resp_login_ajax import resp_login_ajax
from src.views.resp_logout import resp_logout
from src.views.resp_test1 import resp_test1
from src.views.resp_test2 import resp_test2
from src.views.resp_migrate import resp_migrate
from src.views.resp_task_service_js import resp_task_service_js
from src.views.resp_ajax_tasks import resp_ajax_tasks
from src.views.resp_app_js import resp_app_js
from src.views.resp_ins_task import resp_ins_task
from src.views.resp_ajax_del_task import resp_ajax_del_task
from src.views.resp_ajax_edit_task import resp_ajax_edit_task
from src.views.resp_ajax_tasks_search import resp_ajax_tasks_search
from src.views.resp_ajax_ins_task import resp_ajax_ins_task
from src.views.resp_ajax_paginated_tasks import resp_ajax_paginated_tasks
from src.views.resp_log_service_js import resp_log_service_js
from src.views.resp_save_log import resp_save_log
from src.views.resp_secret_page_css import resp_secret_page_css


class FrontController:
    def __init__(self, environ, response):
        self.environ = environ
        self.response = response

    # Workarround for the issue with missing favicon.ico:
    @classmethod
    def handle_favicon(cls, environ, response):
        if environ['PATH_INFO'] == '/favicon.ico':
            return resp_favicon(response)

    @classmethod
    def handle_not_found(cls, response):
        return resp_not_found(response)

    @classmethod
    def handle_main_css(cls, environ, response):
        if environ['PATH_INFO'] == '/static/css/main.css':
            return resp_main_css(response)

    @classmethod
    def handle_secret_page_css(cls, environ, response):
        if environ['PATH_INFO'] == '/static/css/secret_page.css':
            return resp_secret_page_css(response)

    @classmethod
    def handle_auth_service_js(cls, environ, response):
        if environ['PATH_INFO'] == '/static/js/AuthService.js':
            return resp_auth_service_js(response)

    @classmethod
    def handle_home(cls, environ, response):
        if environ['PATH_INFO'] == '/':
            return resp_home(environ, response)

    @classmethod
    def login_form(cls, environ, response):
        if environ['PATH_INFO'] == '/login_form':
            return resp_login_form(response)

    @classmethod
    def handle_secret_pg(cls, environ, response):
        if environ['PATH_INFO'] == '/secret':
            return resp_secret_pg(environ, response)

    @classmethod
    def login_ajax(cls, environ, response):
        if environ['PATH_INFO'] == '/login_ajax':
            return resp_login_ajax(environ, response)

    @classmethod
    def logout(cls, environ, response):
        if environ['PATH_INFO'] == '/logout':
            return resp_logout(environ, response)

    @classmethod
    def handle_migrate(cls, environ, response):
        if environ['PATH_INFO'] == '/migrate':
            return resp_migrate(response)

    @classmethod
    def handle_task_service_js(cls, environ, response):
        if environ['PATH_INFO'] == '/static/js/TaskService.js':
            return resp_task_service_js(response)

    @classmethod
    def handle_app_js(cls, environ, response):
        if environ['PATH_INFO'] == '/static/js/app.js':
            return resp_app_js(response)

    @classmethod
    def handle_log_service_js(cls, environ, response):
        if environ['PATH_INFO'] == '/static/js/LogService.js':
            return resp_log_service_js(response)

    @classmethod
    def handle_ajax_tasks(cls, environ, response):
        if environ['PATH_INFO'] == '/ajax_tasks':
            return resp_ajax_tasks(response)

    @classmethod
    def handle_ajax_paginated_tasks(cls, environ, response):
        if environ['PATH_INFO'] == '/ajax_paginated_tasks':
            return resp_ajax_paginated_tasks(environ, response)

    @classmethod
    def handle_ins_task(cls, environ, response):
        if environ['PATH_INFO'] == '/ins_task':
            return resp_ins_task(environ, response)

    @classmethod
    def handle_ajax_ins_task(cls, environ, response):
        if environ['PATH_INFO'] == '/ajax_ins_task':
            return resp_ajax_ins_task(environ, response)

    @classmethod
    def handle_ajax_del_task(cls, environ, response):
        if environ['PATH_INFO'] == '/ajax_del_task':
            return resp_ajax_del_task(environ, response)

    @classmethod
    def handle_ajax_edit_task(cls, environ, response):
        if environ['PATH_INFO'] == '/ajax_edit_task':
            return resp_ajax_edit_task(environ, response)

    @classmethod
    def handle_ajax_tasks_search(cls, environ, response):
        if environ['PATH_INFO'] == '/ajax_tasks_search':
            return resp_ajax_tasks_search(environ, response)

    @classmethod
    def handle_save_log(cls, environ, response):
        if environ['PATH_INFO'] == '/save_log':
            return resp_save_log(environ, response)

    @classmethod
    def test1(cls, environ, response):
        if environ['PATH_INFO'] == '/test1':
            return resp_test1(response)

    @classmethod
    def test2(cls, environ, response):
        if environ['PATH_INFO'] == '/test2':
            return resp_test2(response)


