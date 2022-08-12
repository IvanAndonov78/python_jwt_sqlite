from src.core_module import core


def resp_task_service_js(response):
    if response is not None:
        js_file_path = 'src/static/js/TaskService.js'
        status = '200 OK'
        headers = [('Content-Type', 'text/javascript')]
        response(status, headers)
        out = core.render(js_file_path)
        response = ''.join([out])
        return [response.encode()]
    else:
        return None

