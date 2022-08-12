from os import environ
from urllib import response

from src.controllers.front_controller import FrontController

fc = FrontController(environ, response)

app_routes = {
    '/': fc.handle_home,
    '/favicon.ico': fc.handle_favicon,
    '/not_found': fc.handle_not_found,
    '/static/css/main.css': fc.handle_main_css,
    '/static/css/secret_page.css': fc.handle_secret_page_css,
    '/static/js/AuthService.js': fc.handle_auth_service_js,
    '/login_form': fc.login_form,
    '/login_ajax': fc.login_ajax,
    '/logout': fc.logout,
    '/secret': fc.handle_secret_pg,
    '/migrate': fc.handle_migrate,
    '/static/js/TaskService.js': fc.handle_task_service_js,
    '/static/js/app.js': fc.handle_app_js,
    '/ajax_tasks': fc.handle_ajax_tasks,
    '/ajax_paginated_tasks': fc.handle_ajax_paginated_tasks,
    '/ins_task': fc.handle_ins_task,
    '/ajax_ins_task': fc.handle_ajax_ins_task,
    '/ajax_del_task': fc.handle_ajax_del_task,
    '/ajax_edit_task': fc.handle_ajax_edit_task,
    '/ajax_tasks_search': fc.handle_ajax_tasks_search,
    '/static/js/LogService.js': fc.handle_log_service_js,
    '/save_log': fc.handle_save_log,
    '/test1': fc.test1,
    '/test2': fc.test2

}


