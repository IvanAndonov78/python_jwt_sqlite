from src.core_module import core
# from wsgiref import util
#
#
# def resp_log_service_js(response):
#     app_js = 'src/static/js/LogService.js'
#     status = '200 OK'
#     headers = [('Content-Type', 'text/javascript')]
#     response(status, headers)
#     return util.FileWrapper(open(app_js, "rb"))


def resp_log_service_js(response):
    if response is not None:
        js_file_path = 'src/static/js/LogService.js'
        status = '200 OK'
        headers = [('Content-Type', 'text/javascript')]
        response(status, headers)
        out = core.render(js_file_path)
        response = ''.join([out])
        return [response.encode()]
    else:
        return None


